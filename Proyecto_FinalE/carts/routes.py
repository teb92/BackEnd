from datetime import datetime
import uuid

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from extensions import cache, cache_key_prefix
from carts.dao import (
    create_or_get_cart_db, add_item_db, update_item_db,
    delete_item_db, get_cart_db, checkout_cart_db
)

bp = Blueprint("carts", __name__)

def _uid_from_jwt() -> int:
    identity = get_jwt_identity()
    try:
        return int(identity)
    except (TypeError, ValueError):
        return int(get_jwt()["uid"])

@bp.post("")
@jwt_required()
def create_or_get_cart():
    user_id = _uid_from_jwt()
    cart, created = create_or_get_cart_db(user_id)
    return jsonify(cart.to_dict()), (201 if created else 200)

@bp.post("/<int:cart_id>/items")
@jwt_required()
def add_item(cart_id: int):
    user_id = _uid_from_jwt()
    data = request.get_json() or {}
    product_id = data.get("product_id")
    qty = data.get("quantity")

    if not isinstance(product_id, int) or not isinstance(qty, int) or qty <= 0:
        return {"error": "product_id (int) y quantity (int>0) son requeridos"}, 400

    cart, err = add_item_db(cart_id, user_id, product_id, qty)
    if err:
        status, payload = err
        return payload, status

    return {"cart": cart.to_dict()}, 200

@bp.patch("/<int:cart_id>/items/<int:item_id>")
@jwt_required()
def update_item(cart_id: int, item_id: int):
    user_id = _uid_from_jwt()
    data = request.get_json() or {}
    qty = data.get("quantity")
    if not isinstance(qty, int) or qty <= 0:
        return {"error": "quantity (int>0) es requerido"}, 400

    cart, err = update_item_db(cart_id, user_id, item_id, qty)
    if err:
        status, payload = err
        return payload, status

    return {"cart": cart.to_dict()}, 200

@bp.delete("/<int:cart_id>/items/<int:item_id>")
@jwt_required()
def delete_item(cart_id: int, item_id: int):
    user_id = _uid_from_jwt()
    cart, err = delete_item_db(cart_id, user_id, item_id)
    if err:
        status, payload = err
        return payload, status
    return {"cart": cart.to_dict()}, 200

@bp.get("/<int:cart_id>")
@jwt_required()
def get_cart(cart_id: int):
    user_id = _uid_from_jwt()
    cart, err = get_cart_db(cart_id, user_id)
    if err:
        status, payload = err
        return payload, status
    return {"cart": cart.to_dict()}, 200

@bp.post("/<int:cart_id>/checkout")
@jwt_required()
def checkout(cart_id: int):
    user_id = _uid_from_jwt()
    data = request.get_json() or {}

    order, invoice, payment, cart, err = checkout_cart_db(cart_id, user_id, data)
    if err:
        status, payload = err
        return payload, status

    try:
        prefix = cache_key_prefix(current_app)
        cache.delete(f"{prefix}products:all")
        from extensions import delete_pattern
        delete_pattern(f"{prefix}products:list*")
        for it in cart.items:
            cache.delete(f"{prefix}product:{it.product_id}")
    except Exception:
        pass

    return {
        "order": {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_cents": order.total_cents
        },
        "invoice": {
            "id": invoice.id,
            "number": invoice.number,
            "issued_at": invoice.issued_at.isoformat(),
            "total_cents": invoice.total_cents
        },
        "payment": {
            "method": payment.method,
            "reference": payment.reference,
            "amount_cents": payment.amount_cents
        },
        "cart": {
            "id": cart.id,
            "status": cart.status
        }
    }, 201
