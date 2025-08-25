
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import asc, desc
from extensions import db, cache, cache_key_prefix, delete_pattern
from models import User
from auth.guards import role_required

bp = Blueprint("users", __name__)


def _k_list():
    args = request.args
    parts = [
        f"{cache_key_prefix(current_app)}users:list",
        f"q={args.get('q','')}",
        f"page={args.get('page','1')}",
        f"page_size={args.get('page_size','20')}",
        f"sort={args.get('sort','created_at')}",
        f"dir={args.get('dir','desc')}",
    ]
    return "|".join(parts)

def _k_detail(uid: int):
    return f"{cache_key_prefix(current_app)}user:{uid}"

def _invalidate_users(user_id: int | None = None):
    delete_pattern(f"{cache_key_prefix(current_app)}users:list*")
    if user_id:
        cache.delete(_k_detail(user_id))

def _to_dict(u: User):
    return {
        "id": u.id,
        "email": u.email,
        "role": u.role,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }

# ---- endpoints ----

@bp.get("/users")
@jwt_required()
@role_required("ADMIN")
@cache.cached(timeout=60, key_prefix=_k_list)
def list_users():
    q = (request.args.get("q") or "").strip()
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 100)
    sort = request.args.get("sort", "created_at")
    direction = request.args.get("dir", "desc").lower()

    query = User.query
    if q:
        like = f"%{q}%"
        query = query.filter(User.email.ilike(like))

    sortable = {"created_at": User.created_at, "email": User.email, "id": User.id}
    col = sortable.get(sort, User.created_at)
    query = query.order_by(desc(col) if direction == "desc" else asc(col))

    items = query.paginate(page=page, per_page=page_size, error_out=False)
    return jsonify({
        "items": [_to_dict(u) for u in items.items],
        "page": page,
        "page_size": page_size,
        "total": items.total,
        "pages": items.pages,
    })

@bp.get("/users/<int:user_id>")
@jwt_required()
@cache.cached(timeout=60, key_prefix=lambda: _k_detail(request.view_args["user_id"]))
def get_user(user_id: int):
    claims = get_jwt()
    role = claims.get("role")
    uid = int(claims.get("uid"))

    if role != "ADMIN" and uid != user_id:
        return jsonify({"error": "forbidden"}), 403

    u = User.query.get_or_404(user_id)
    return jsonify(_to_dict(u))

@bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id: int):
    claims = get_jwt()
    role = claims.get("role")
    uid = int(claims.get("uid"))

    if role != "ADMIN" and uid != user_id:
        return jsonify({"error": "forbidden"}), 403

    u = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    if "password" in data and data["password"]:
        from extensions import bcrypt
        u.password_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    if role == "ADMIN" and "role" in data:
        new_role = str(data["role"]).upper()
        if new_role not in {"ADMIN", "CUSTOMER"}:
            return jsonify({"error": "invalid role"}), 400
        u.role = new_role

    db.session.commit()
    _invalidate_users(user_id)
    return jsonify(_to_dict(u))
