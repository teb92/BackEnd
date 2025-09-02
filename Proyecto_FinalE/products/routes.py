from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from extensions import cache, cache_key_prefix, delete_pattern
from models import Product
from auth.guards import role_required
from products.dao import (
    list_products_db, get_product_by_id_db,
    create_product_db, update_product_db, delete_product_db
)

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


@bp.get("/products")
@cache.cached(timeout=60, key_prefix=_k_list)
def list_products():
    q = (request.args.get("q") or "").strip()
    active = request.args.get("active")
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 20)), 100)
    sort = request.args.get("sort", "created_at")
    direction = request.args.get("dir", "desc").lower()

    items, total, pages = list_products_db(q, active, page, page_size, sort, direction)
    return jsonify({
        "items": [_to_dict(p) for p in items],
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
    })

@bp.get("/products/<int:product_id>")
@cache.cached(timeout=120, key_prefix=lambda: _k_detail(request.view_args["product_id"]))
def get_product(product_id: int):
    p = get_product_by_id_db(product_id)
    return jsonify(_to_dict(p))

@bp.post("/products")
@jwt_required()
@role_required("ADMIN")
def create_product():
    data = request.get_json() or {}
    p, err = create_product_db(data)
    if err:
        status, payload = err
        return payload, status

    _invalidate_products(p.id)
    return jsonify(_to_dict(p)), 201

@bp.put("/products/<int:product_id>")
@bp.patch("/products/<int:product_id>")
@jwt_required()
@role_required("ADMIN")
def update_product(product_id: int):
    data = request.get_json() or {}
    p, err = update_product_db(product_id, data)
    if err:
        status, payload = err
        return payload, status

    _invalidate_products(p.id)
    return jsonify(_to_dict(p))

@bp.delete("/products/<int:product_id>")
@jwt_required()
@role_required("ADMIN")
def delete_product(product_id: int):
    delete_product_db(product_id)
    _invalidate_products(product_id)
    return jsonify({"ok": True})
