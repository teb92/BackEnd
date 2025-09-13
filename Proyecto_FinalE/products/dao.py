from typing import Tuple
from sqlalchemy import asc, desc, or_
from extensions import db
from models import Product

def list_products_db(q: str, active: str, page: int, page_size: int, sort: str, direction: str):

    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Product.name.ilike(like), Product.sku.ilike(like)))
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
    return items.items, items.total, items.pages

def get_product_by_id_db(product_id: int) -> Product:
    return Product.query.get_or_404(product_id)

def create_product_db(data: dict):
    required = ["sku", "name", "price_cents", "stock"]
    missing = [k for k in required if data.get(k) in (None, "")]
    if missing:
        return None, (400, {"error": f"Missing fields: {', '.join(missing)}"})

    if Product.query.filter_by(sku=(data["sku"] or "").strip()).first():
        return None, (409, {"error": "SKU already exists"})

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
    return p, None

def update_product_db(product_id: int, data: dict):
    p = Product.query.get_or_404(product_id)

    if "sku" in data:
        new_sku = (data["sku"] or "").strip()
        if new_sku and new_sku != p.sku and Product.query.filter_by(sku=new_sku).first():
            return None, (409, {"error": "SKU already exists"})
        p.sku = new_sku or p.sku

    if "name" in data: p.name = (data["name"] or "").strip()
    if "description" in data: p.description = (data["description"] or "").strip() or None
    if "price_cents" in data: p.price_cents = int(data["price_cents"])
    if "stock" in data: p.stock = int(data["stock"])
    if "active" in data: p.active = bool(data["active"])

    db.session.commit()
    return p, None

def delete_product_db(product_id: int) -> None:
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
