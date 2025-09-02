from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from auth.dao import register_user_db, verify_credentials_db 

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password")
    role = (data.get("role") or "CUSTOMER").upper()

    u, err = register_user_db(email=email, password=password, role=role)
    if err:
        status, payload = err
        return payload, status

    return {"id": u.id, "email": u.email, "role": u.role}, 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    u = verify_credentials_db(email=email, password=password)
    if not u:
        return {"error": "invalid credentials"}, 401

    claims = {"role": u.role, "uid": u.id}
    token = create_access_token(identity=str(u.id), additional_claims=claims)
    return {"access_token": token, "role": u.role}

@bp.get("/me")
@jwt_required()
def me():
    claims = get_jwt()
    return {"user_id": claims["uid"], "role": claims["role"]}