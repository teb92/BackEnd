from typing import Tuple, Optional
from extensions import db, bcrypt
from models import User

VALID_ROLES = {"ADMIN", "CUSTOMER"}

def find_user_by_email_db(email: str) -> Optional[User]:
    return User.query.filter_by(email=email).first()

def register_user_db(email: str, password: str, role: str) -> Tuple[Optional[User], Optional[Tuple[int, dict]]]:

    if not email or not password:
        return None, (400, {"error": "email and password required"})
    role = (role or "CUSTOMER").upper()
    if role not in VALID_ROLES:
        return None, (400, {"error": "invalid role"})

    if find_user_by_email_db(email):
        return None, (409, {"error": "email already registered"})

    u = User(email=email.strip().lower(), role=role)
    if hasattr(u, "set_password"):
        u.set_password(password)
    else:
        u.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    db.session.add(u)
    db.session.commit()
    return u, None

def verify_credentials_db(email: str, password: str) -> Optional[User]:
    u = find_user_by_email_db(email.strip().lower())
    if not u:
        return None

    if hasattr(u, "check_password"):
        return u if u.check_password(password or "") else None
    else:
        from werkzeug.security import check_password_hash
        return u if check_password_hash(u.password_hash, password or "") else None