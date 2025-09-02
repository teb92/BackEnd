from datetime import datetime
import uuid
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import (
    Cart, CartItem, Product,
    Order, OrderItem, Invoice, Payment, Address
)

def create_or_get_cart_db(user_id: int) -> tuple[Cart, bool]:
    cart = Cart.query.filter_by(user_id=user_id, status="OPEN").first()
    created = False
    if not cart:
        cart = Cart(user_id=user_id, status="OPEN")
        db.session.add(cart)
        db.session.commit()
        created = True
    return cart, created

def add_item_db(cart_id: int, user_id: int, product_id: int, qty: int):
    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return None, (404, {"error": "cart not found"})
    if cart.status != "OPEN":
        return None, (409, {"error": "cart is not OPEN"})

    product = Product.query.get(product_id)
    if not product or not product.active:
        return None, (404, {"error": "product not found or inactive"})

    existing = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    new_total_qty = (existing.quantity if existing else 0) + qty
    if product.stock < new_total_qty:
        return None, (422, {"error": "insufficient stock", "available": product.stock})

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
    return cart, None

def update_item_db(cart_id: int, user_id: int, item_id: int, qty: int):
    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return None, (404, {"error": "cart not found"})
    if cart.status != "OPEN":
        return None, (409, {"error": "cart is not OPEN"})

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return None, (404, {"error": "item not found"})

    product = item.product
    if product.stock < qty:
        return None, (422, {"error": "insufficient stock", "available": product.stock})

    item.quantity = qty
    db.session.commit()
    return cart, None

def delete_item_db(cart_id: int, user_id: int, item_id: int):
    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return None, (404, {"error": "cart not found"})
    if cart.status != "OPEN":
        return None, (409, {"error": "cart is not OPEN"})

    item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not item:
        return None, (404, {"error": "item not found"})

    db.session.delete(item)
    db.session.commit()
    return cart, None

def get_cart_db(cart_id: int, user_id: int):
    cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
    if not cart:
        return None, (404, {"error": "cart not found"})
    return cart, None

def checkout_cart_db(cart_id: int, user_id: int, data: dict):
    try:
        cart: Cart | None = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
        if not cart:
            return None, (404, {"error": "cart not found"})
        if cart.status != "OPEN":
            return None, (409, {"error": "cart is not OPEN"})
        if not cart.items:
            return None, (422, {"error": "cart is empty"})

        pay = (data.get("payment") or {})
        reference = pay.get("reference")
        if not reference:
            return None, (400, {"error": "payment.reference is required"})

        subtotal = 0
        for it in cart.items:
            product = Product.query.get(it.product_id)
            if not product or not product.active:
                return None, (422, {"error": f"product {it.product_id} not found or inactive"})
            if product.stock < it.quantity:
                return None, (422, {"error": f"insufficient stock for product {product.id}"})

        for it in cart.items:
            product = Product.query.get(it.product_id)
            product.stock -= it.quantity
            subtotal += it.quantity * it.unit_price_cents

        address_id = data.get("address_id")
        if address_id:
            billing_address = Address.query.filter_by(id=address_id, user_id=user_id).first()
            if not billing_address:
                return None, (422, {"error": "billing address not found for user"})
        else:
            addr = data.get("billing_address") or {}
            if not addr.get("line1") or not addr.get("city"):
                return None, (422, {"error": "billing_address.line1 and city required"})
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
        return order, invoice, payment, cart, None

    except IntegrityError as ie:
        db.session.rollback()
        return None, None, None, None, (400, {"error": "integrity error", "detail": str(ie.orig)})
    except Exception as e:
        db.session.rollback()
        return None, None, None, None, (500, {"error": "unexpected error", "detail": str(e)})
