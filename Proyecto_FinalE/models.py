
from datetime import datetime
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from extensions import db, bcrypt 


user_role = ENUM("ADMIN", "CUSTOMER", name="user_role", create_type=False)
cart_status = ENUM("OPEN", "CONVERTED", "ABANDONED", name="cart_status", create_type=False)
order_status = ENUM("PENDING", "PAID", "CANCELLED", "REFUNDED", name="order_status", create_type=False)
address_type = ENUM("BILLING", "SHIPPING", name="address_type", create_type=False)
payment_method = ENUM("SINPE", name="payment_method", create_type=False)
return_status = ENUM("REQUESTED", "APPROVED", "REJECTED", "REFUNDED", name="return_status", create_type=False)

SCHEMA = "ECommercePets"


# USER
class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(user_role, nullable=False, default="CUSTOMER")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    carts = db.relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")
    addresses = db.relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, raw: str):
        self.password_hash = bcrypt.generate_password_hash(raw).decode("utf-8")

    def check_password(self, raw: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw)



#  PRODUCT
class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), unique=True, index=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price_cents = db.Column(db.Integer, nullable=False)  
    stock = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")


# CART
class Cart(db.Model):
    __tablename__ = "carts"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{SCHEMA}.users.id"),
        nullable=False,
        index=True
    )
    status = db.Column(cart_status, nullable=False, default="OPEN")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="carts")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    # Helpers
    def total_cents(self) -> int:
        return sum((ci.quantity * ci.unit_price_cents) for ci in (self.items or []))

    def item_count(self) -> int:
        return sum(ci.quantity for ci in (self.items or []))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "item_count": self.item_count(),
            "total_cents": self.total_cents(),
            "items": [it.to_dict() for it in (self.items or [])]
        }


class CartItem(db.Model):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_item_cart_product"),
        CheckConstraint("quantity > 0", name="ck_cart_items_qty_positive"),
        CheckConstraint("unit_price_cents >= 0", name="ck_cart_items_price_nonneg"),
        {'schema': SCHEMA}
    )

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{SCHEMA}.carts.id"),
        nullable=False,
        index=True
    )
    product_id = db.Column(
        db.Integer,
        db.ForeignKey(f"{SCHEMA}.products.id"),
        nullable=False,
        index=True
    )
   
    unit_price_cents = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", back_populates="cart_items")

    def line_total_cents(self) -> int:
        return self.quantity * self.unit_price_cents

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price_cents": self.unit_price_cents,
            "line_total_cents": self.line_total_cents(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "product": {
                "id": self.product.id,
                "name": getattr(self.product, "name", None),
                "sku": getattr(self.product, "sku", None),
            } if self.product else None
        }


#  ORDER

class Order(db.Model):
    __tablename__ = "orders"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(32), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.id"), nullable=False, index=True)
    cart_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.carts.id"), nullable=True)
    billing_address_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.addresses.id"), nullable=True)
    status = db.Column(order_status, nullable=False, default="PENDING")

    subtotal_cents = db.Column(db.Integer, nullable=False, default=0)
    tax_cents = db.Column(db.Integer, nullable=False, default=0)
    total_cents = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="orders")
    cart = db.relationship("Cart")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    invoice = db.relationship("Invoice", back_populates="order", uselist=False, cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    billing_address = db.relationship("Address")


class OrderItem(db.Model):
    __tablename__ = "order_items"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.orders.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.products.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_cents = db.Column(db.Integer, nullable=False)  

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")


# INVOICE

class Invoice(db.Model):
    __tablename__ = "invoices"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.orders.id"), unique=True, nullable=False)
    number = db.Column(db.String(32), unique=True, index=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_cents = db.Column(db.Integer, nullable=False)

    order = db.relationship("Order", back_populates="invoice")

# PAYMENT
class Payment(db.Model):
    __tablename__ = "payments"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.orders.id"), nullable=False, index=True)
    method = db.Column(payment_method, nullable=False, default="SINPE")
    reference = db.Column(db.String(64), nullable=False)  
    amount_cents = db.Column(db.Integer, nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    order = db.relationship("Order", back_populates="payments")


# ADDRESS
class Address(db.Model):
    __tablename__ = "addresses"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.users.id"), nullable=False, index=True)
    type = db.Column(address_type, nullable=False)  
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(2), nullable=False, default="CR")

    user = db.relationship("User", back_populates="addresses")

# RETURN
class Return(db.Model):
    __tablename__ = "returns"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.orders.id"), nullable=False, index=True)
    status = db.Column(return_status, nullable=False, default="REQUESTED")
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    order = db.relationship("Order")
    items = db.relationship("ReturnItem", back_populates="return_", cascade="all, delete-orphan")


class ReturnItem(db.Model):
    __tablename__ = "return_items"
    __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.returns.id"), nullable=False, index=True)
    order_item_id = db.Column(db.Integer, db.ForeignKey(f"{SCHEMA}.order_items.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)

    return_ = db.relationship("Return", back_populates="items")
    order_item = db.relationship("OrderItem")
