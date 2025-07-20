from jwt_manager import JWT_Manager
from flask import Flask, request, Response, jsonify
from db import Base, engine
from models import Product
from db import SessionLocal
from models import User
from models import Invoice
from datetime import datetime


Base.metadata.create_all(bind=engine)


app = Flask(__name__)

jwt_manager = JWT_Manager()


@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get("username") or not data.get("password") or not data.get("role"):
        return Response("Missing data", status=400)

    with SessionLocal() as session:
        new_user = User(
            username=data["username"],
            password=data["password"],
            role=data["role"]
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        token = jwt_manager.encode({
            "id": new_user.id,
            "username": new_user.username,
            "role": new_user.role
        })

        return jsonify(token=token)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get("username") or not data.get("password"):
        return Response("Missing credentials", status=400)

    with SessionLocal() as session:
        user = session.query(User).filter_by(
            username=data["username"],
            password=data["password"]
        ).first()

        if not user:
            return Response("Invalid credentials", status=403)

        token = jwt_manager.encode({
            "id": user.id,
            "username": user.username,
            "role": user.role
        })

        return jsonify(token=token)

@app.route('/me')
def me():
    try:
        token = request.headers.get('Authorization')
        if token:
            decoded = jwt_manager.decode(token.replace("Bearer ", ""))
            user_id = decoded['id']

            with SessionLocal() as session:
                user = session.query(User).filter_by(id=user_id).first()
                if not user:
                    return Response("User not found", status=404)

                return jsonify(id=user.id, username=user.username, role=user.role)
        else:
            return Response("Missing token", status=403)
    except Exception as e:
        return Response("Internal server error", status=500)
    

def get_current_user():
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    token = token.split(" ")[1]
    return jwt_manager.decode(token)

@app.route("/products", methods=["GET"])
def list_products():
    with SessionLocal() as db:
        products = db.query(Product).all()
    result = [{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "entry_date": p.entry_date.isoformat(),
        "quantity": p.quantity
    } for p in products]
    return jsonify(result)

@app.route("/products", methods=["POST"])
def create_product():
    user = get_current_user()
    if not user or user["role"] != "admin":
        return Response("Unauthorized", status=403)
    
    data = request.get_json()
    with SessionLocal() as db:
        new_product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"]
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
    return jsonify({"message": "Product created", "id": new_product.id})

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    user = get_current_user()
    if not user or user["role"] != "admin":
        return Response("Unauthorized", status=403)
    
    data = request.get_json()
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return Response("Product not found", status=404)

        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        db.commit()
    return jsonify({"message": "Product updated"})

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    user = get_current_user()
    if not user or user["role"] != "admin":
        return Response("Unauthorized", status=403)

    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return Response("Product not found", status=404)

        db.delete(product)
        db.commit()
    return jsonify({"message": "Product deleted"})

@app.route("/purchase", methods=["POST"])
def purchase():
    user = get_current_user()
    if not user:
        return Response("Unauthorized", status=403)
    
    data = request.get_json()
    if not data or not isinstance(data, list):
        return Response("Incomplete or invalid data", status=400)
    
    with SessionLocal() as db:
        invoices_created = []
        
        for item in data:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            
            if product_id is None or quantity is None or quantity <= 0:
                return Response("Invalid product_id or quantity", status=400)
            
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return Response(f"Product with id {product_id} not found", status=404)
            
            if product.quantity < quantity:
                return Response(f"Insufficient stock for product id {product_id}", status=400)
            product.quantity -= quantity
            
            total = product.price * quantity
            
            invoice = Invoice(
                user_id=user["id"],
                product_id=product_id,
                quantity=quantity,
                total=total,
                date=datetime.utcnow()
            )
            db.add(invoice)
            invoices_created.append(invoice)
        
        db.commit()
        for inv in invoices_created:
            db.refresh(inv)
    
    return jsonify({
        "message": "Purchase successful",
        "invoices": [{"invoice_id": inv.id, "product_id": inv.product_id, "quantity": inv.quantity} for inv in invoices_created]
    })


@app.route("/invoices", methods=["GET"])
def list_invoices():
    user = get_current_user()
    if not user:
        return Response("Unauthorized", status=403)
    
    with SessionLocal() as db:
        invoices = db.query(Invoice).filter(Invoice.user_id == user["id"]).all()
    
    result = [{
        "id": inv.id,
        "product_id": inv.product_id,
        "quantity": inv.quantity,
        "total": inv.total,
        "date": inv.date.isoformat()
    } for inv in invoices]

    return jsonify(result)####

app.run(host='localhost', port=5500, debug=True) 