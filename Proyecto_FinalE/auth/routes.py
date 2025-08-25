
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from extensions import db
from models import User

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    role = (data.get("role") or "CUSTOMER").upper()
    if not email or not password:
        return {"error": "email and password required"}, 400
    if role not in ("ADMIN", "CUSTOMER"):
        return {"error": "invalid role"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "email already registered"}, 409

    u = User(email=email, role=role)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return {"id": u.id, "email": u.email, "role": u.role}, 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password):
        return {"error": "invalid credentials"}, 401

    claims = {"role": u.role, "uid": u.id}
    token = create_access_token(identity=str(u.id), additional_claims=claims)
    return {"access_token": token, "role": u.role}

@bp.get("/me")
@jwt_required()
def me():
    claims = get_jwt()
    return {"user_id": claims["uid"], "role": claims["role"]}
