# users/dao.py
from typing import Tuple, Optional
from sqlalchemy import asc, desc
from extensions import db, bcrypt
from models import User

def list_users_db(q: str, page: int, page_size: int, sort: str, direction: str):
    query = User.query
    if q:
        like = f"%{q}%"
        query = query.filter(User.email.ilike(like))

    sortable = {"created_at": User.created_at, "email": User.email, "id": User.id}
    col = sortable.get(sort, User.created_at)
    query = query.order_by(desc(col) if direction.lower() == "desc" else asc(col))

    items = query.paginate(page=page, per_page=page_size, error_out=False)
    return items.items, items.total, items.pages

def get_user_by_id_db(user_id: int) -> User:
    return User.query.get_or_404(user_id)

def update_user_db(user_id: int, data: dict, can_change_role: bool) -> Tuple[Optional[User], Optional[Tuple[int, dict]]]:
    u = User.query.get_or_404(user_id)

    pwd = data.get("password")
    if pwd:
        u.password_hash = bcrypt.generate_password_hash(pwd).decode("utf-8")

    if can_change_role and "role" in data:
        new_role = str(data["role"]).upper()
        if new_role not in {"ADMIN", "CUSTOMER"}:
            return None, (400, {"error": "invalid role"})
        u.role = new_role

    db.session.commit()
    return u, None