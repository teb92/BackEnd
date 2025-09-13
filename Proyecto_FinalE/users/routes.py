from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import asc, desc  # (ya no se usa directamente, pero puedes quitarlo si prefieres)
from extensions import db, cache, cache_key_prefix, delete_pattern
from models import User
from auth.guards import role_required
from users.dao import list_users_db, get_user_by_id_db, update_user_db

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

    items, total, pages = list_users_db(q=q, page=page, page_size=page_size, sort=sort, direction=direction)
    return jsonify({
        "items": [_to_dict(u) for u in items],
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
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

    u = get_user_by_id_db(user_id)
    return jsonify(_to_dict(u))

@bp.put("/users/<int:user_id>")
@jwt_required()
def update_user(user_id: int):
    claims = get_jwt()
    role = claims.get("role")
    uid = int(claims.get("uid"))

    if role != "ADMIN" and uid != user_id:
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json() or {}
    can_change_role = (role == "ADMIN")
    u, err = update_user_db(user_id=user_id, data=data, can_change_role=can_change_role)
    if err:
        status, payload = err
        return jsonify(payload), status

    db.session.commit()  # (no es estrictamente necesario, update_user_db ya hace commit)
    _invalidate_users(user_id)
    return jsonify(_to_dict(u))