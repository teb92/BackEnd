
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import asc, desc
from extensions import db, cache, cache_key_prefix, delete_pattern
from models import Product
from auth.guards import role_required

bp = Blueprint("products", __name__)


def _to_dict(p: Product):
    return {
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "description": p.description,
        "price_cents": p.price_cents,
        "stock": p.stock,
        "active": p.active,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }

def _k_list():
    args = request.args
    parts = [
        f"{cache_key_prefix(current_app)}products:list",
        f"q={args.get('q','')}",
        f"active={args.get('active','')}",
        f"page={args.get('page','1')}",
        f"page_size={args.get('page_size','20')}",
        f"sort={args.get('sort','created_at')}",
        f"dir={args.get('dir','desc')}",
    ]
    return "|".join(parts)

def _k_detail(pid: int):
    return f"{cache_key_prefix(current_app)}product:{pid}"

def _invalidate_products(product_id: int | None = None):
    delete_pattern(f"{cache_key_prefix(current_app)}products:list*")
    if product_id:
        cache.delete(_k_detail(product_id))

# ---------- Endpoints ----------
@bp.get("/products")
@cache.cached(timeout=60, key_prefix=_k_list)  
def list_products():
    q = (request.args.get("q") or "").strip()
    active = request.args.get("active")
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 100)
    sort = request.args.get("sort", "created_at")
    direction = request.args.get("dir", "desc").lower()

    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Product.name.ilike(like), Product.sku.ilike(like)))
    if active in ("true", "false"):
        query = query.filter(Product.active.is_(active == "true"))

    sortable = {
        "created_at": Product.created_at,
        "updated_at": Product.updated_at,
        "name": Product.name,
        "price_cents": Product.price_cents,
        "stock": Product.stock,
        "sku": Product.sku,
    }
    col = sortable.get(sort, Product.created_at)
    query = query.order_by(desc(col) if direction == "desc" else asc(col))

    items = query.paginate(page=page, per_page=page_size, error_out=False)
    return jsonify({
        "items": [_to_dict(p) for p in items.items],
        "page": page,
        "page_size": page_size,
        "total": items.total,
        "pages": items.pages,
    })

@bp.get("/products/<int:product_id>")
@cache.cached(timeout=120, key_prefix=lambda: _k_detail(request.view_args["product_id"]))
def get_product(product_id: int):
    p = Product.query.get_or_404(product_id)
    return jsonify(_to_dict(p))

@bp.post("/products")
@jwt_required()
@role_required("ADMIN")
def create_product():
    data = request.get_json() or {}
    required = ["sku", "name", "price_cents", "stock"]
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400

    if Product.query.filter_by(sku=(data["sku"] or "").strip()).first():
        return {"error": "SKU already exists"}, 409

    p = Product(
        sku=data["sku"].strip(),
        name=data["name"].strip(),
        description=(data.get("description") or "").strip() or None,
        price_cents=int(data["price_cents"]),
        stock=int(data["stock"]),
        active=bool(data.get("active", True)),
    )
    db.session.add(p)
    db.session.commit()

    _invalidate_products(p.id)
    return jsonify(_to_dict(p)), 201

@bp.put("/products/<int:product_id>")
@bp.patch("/products/<int:product_id>")
@jwt_required()
@role_required("ADMIN")
def update_product(product_id: int):
    p = Product.query.get_or_404(product_id)
    data = request.get_json() or {}

    if "sku" in data:
        new_sku = (data["sku"] or "").strip()
        if new_sku and new_sku != p.sku and Product.query.filter_by(sku=new_sku).first():
            return {"error": "SKU already exists"}, 409
        p.sku = new_sku or p.sku

    if "name" in data: p.name = (data["name"] or "").strip()
    if "description" in data: p.description = (data["description"] or "").strip() or None
    if "price_cents" in data: p.price_cents = int(data["price_cents"])
    if "stock" in data: p.stock = int(data["stock"])
    if "active" in data: p.active = bool(data["active"])

    db.session.commit()
    _invalidate_products(p.id)
    return jsonify(_to_dict(p))

@bp.delete("/products/<int:product_id>")
@jwt_required()
@role_required("ADMIN")
def delete_product(product_id: int):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    _invalidate_products(product_id)
    return jsonify({"ok": True})
