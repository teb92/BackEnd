
from datetime import datetime
import uuid

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import (
    Cart, CartItem, Product,
    Order, OrderItem, Invoice, Payment, Address
)

bp = Blueprint("carts", __name__)


@bp.post("")
@jwt_required()
def create_or_get_cart():

    identity = get_jwt_identity()  
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    cart = Cart.query.filter_by(user_id=user_id, status="OPEN").first()
    created = False

    if not cart:
        cart = Cart(user_id=user_id, status="OPEN")
        db.session.add(cart)
        db.session.commit()
        created = True

    return jsonify(cart.to_dict()), (201 if created else 200)

@bp.post("/<int:cart_id>/items")
@jwt_required()
def add_item(cart_id: int):

    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    data = request.get_json() or {}
    product_id = data.get("product_id")
    qty = data.get("quantity")


    if not isinstance(product_id, int) or not isinstance(qty, int) or qty <= 0:
        return {"error": "product_id (int) y quantity (int>0) son requeridos"}, 400


    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return {"error": "cart not found"}, 404
    if cart.status != "OPEN":
        return {"error": "cart is not OPEN"}, 409

    product = Product.query.get(product_id)
    if not product or not product.active:
        return {"error": "product not found or inactive"}, 404

    existing = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    new_total_qty = (existing.quantity if existing else 0) + qty
    if product.stock < new_total_qty:
        return {"error": "insufficient stock", "available": product.stock}, 422


    if existing:
        existing.quantity = new_total_qty
    else:
        db.session.add(CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=qty,
            unit_price_cents=product.price_cents  
        ))

    db.session.commit()
    return {"cart": cart.to_dict()}, 200


@bp.patch("/<int:cart_id>/items/<int:item_id>")
@jwt_required()
def update_item(cart_id: int, item_id: int):
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    data = request.get_json() or {}
    qty = data.get("quantity")
    if not isinstance(qty, int) or qty <= 0:
        return {"error": "quantity (int>0) es requerido"}, 400

    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return {"error": "cart not found"}, 404
    if cart.status != "OPEN":
        return {"error": "cart is not OPEN"}, 409

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return {"error": "item not found"}, 404

    product = item.product
    if product.stock < qty:
        return {"error": "insufficient stock", "available": product.stock}, 422

    item.quantity = qty
    db.session.commit()
    return {"cart": cart.to_dict()}, 200


@bp.delete("/<int:cart_id>/items/<int:item_id>")
@jwt_required()
def delete_item(cart_id: int, item_id: int):
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return {"error": "cart not found"}, 404
    if cart.status != "OPEN":
        return {"error": "cart is not OPEN"}, 409

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return {"error": "item not found"}, 404

    db.session.delete(item)
    db.session.commit()
    return {"cart": cart.to_dict()}, 200



@bp.get("/<int:cart_id>")
@jwt_required()
def get_cart(cart_id: int):
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return {"error": "cart not found"}, 404
    return {"cart": cart.to_dict()}, 200



@bp.post("/<int:cart_id>/checkout")
@jwt_required()
def checkout(cart_id: int):

    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        user_id = int(get_jwt()["uid"])

    data = request.get_json() or {}
    pay = (data.get("payment") or {})
    reference = pay.get("reference")
    if not reference:
        return {"error": "payment.reference es requerido"}, 400

    cart: Cart | None = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return {"error": "cart not found"}, 404
    if cart.status != "OPEN":
        return {"error": "cart is not OPEN"}, 409
    if not cart.items:
        return {"error": "cart is empty"}, 422

    try:
        subtotal = 0

        for it in cart.items:
            product = Product.query.get(it.product_id)
            if not product or not product.active:
                raise ValueError(f"product {it.product_id} not found or inactive")
            if product.stock < it.quantity:
                raise ValueError(
                    f"insufficient stock for product {product.id} "
                    f"(available={product.stock}, need={it.quantity})"
                )

        for it in cart.items:
            product = Product.query.get(it.product_id)
            product.stock -= it.quantity
            subtotal += it.quantity * it.unit_price_cents

        address_id = data.get("address_id")
        if address_id:
            billing_address = Address.query.filter_by(id=address_id, user_id=user_id).first()
            if not billing_address:
                raise ValueError("billing address not found for user")
        else:
            addr = data.get("billing_address") or {}
            if not addr.get("line1") or not addr.get("city"):
                raise ValueError("billing_address.line1 y billing_address.city son requeridos si no envías address_id")
            billing_address = Address(
                user_id=user_id,
                type="BILLING",
                line1=addr["line1"],
                line2=addr.get("line2"),
                city=addr["city"],
                region=addr.get("region"),
                postal_code=addr.get("postal_code"),
                country=addr.get("country") or "CR",
            )
            db.session.add(billing_address)
            db.session.flush()


        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{user_id}-{uuid.uuid4().hex[:6].upper()}"
        order = Order(
            order_number=order_number,
            user_id=user_id,
            cart_id=cart.id,
            billing_address_id=billing_address.id,
            status="PAID",
            subtotal_cents=subtotal,
            tax_cents=0,
            total_cents=subtotal,
        )
        db.session.add(order)
        db.session.flush()


        for it in cart.items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=it.product_id,
                quantity=it.quantity,
                unit_price_cents=it.unit_price_cents
            ))


        invoice = Invoice(
            order_id=order.id,
            number=f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order.id}",
            issued_at=datetime.utcnow(),
            total_cents=order.total_cents
        )
        db.session.add(invoice)

        payment = Payment(
            order_id=order.id,
            method="SINPE",
            reference=reference,
            amount_cents=order.total_cents,
            paid_at=datetime.utcnow()
        )
        db.session.add(payment)

        cart.status = "CONVERTED"

        db.session.commit()
        try:
            from extensions import cache, cache_key_prefix
            prefix = cache_key_prefix(current_app)
            cache.delete(f"{prefix}products:all")
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

    except ValueError as ve:
        db.session.rollback()
        return {"error": str(ve)}, 422
    except IntegrityError as ie:
        db.session.rollback()
        return {"error": "integrity error", "detail": str(ie.orig)}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": "unexpected error", "detail": str(e)}, 500
