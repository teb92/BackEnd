# tests/conftest.py
import os
import sys
import pathlib
from datetime import datetime

import pytest
from sqlalchemy import text, event
from sqlalchemy.dialects.postgresql import ENUM


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from extensions import db, bcrypt 
from models import User  

SCHEMA = "ECommercePets"

user_role = ENUM("ADMIN", "CUSTOMER", name="user_role", schema=SCHEMA)
cart_status = ENUM("OPEN", "CONVERTED", "ABANDONED", name="cart_status", schema=SCHEMA)
order_status = ENUM("PENDING", "PAID", "CANCELLED", "REFUNDED", name="order_status", schema=SCHEMA)
address_type = ENUM("BILLING", "SHIPPING", name="address_type", schema=SCHEMA)
payment_method = ENUM("SINPE", name="payment_method", schema=SCHEMA)
return_status = ENUM("REQUESTED", "APPROVED", "REJECTED", "REFUNDED", name="return_status", schema=SCHEMA)

ENUM_DDL = [
    f'CREATE TYPE "{SCHEMA}".user_role AS ENUM (\'ADMIN\', \'CUSTOMER\')',
    f'CREATE TYPE "{SCHEMA}".cart_status AS ENUM (\'OPEN\', \'CONVERTED\', \'ABANDONED\')',
    f'CREATE TYPE "{SCHEMA}".order_status AS ENUM (\'PENDING\', \'PAID\', \'CANCELLED\', \'REFUNDED\')',
    f'CREATE TYPE "{SCHEMA}".address_type AS ENUM (\'BILLING\', \'SHIPPING\')',
    f'CREATE TYPE "{SCHEMA}".payment_method AS ENUM (\'SINPE\')',
    f'CREATE TYPE "{SCHEMA}".return_status AS ENUM (\'REQUESTED\', \'APPROVED\', \'REJECTED\', \'REFUNDED\')',
]

TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "xxx+xx://xx:xx@localhost:xx/ecommercepets_test",
)

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=TEST_DB_URL,
        CACHE_TYPE="SimpleCache",
        CACHE_DEFAULT_TIMEOUT=60,
        JWT_SECRET_KEY="test-secret",
    )

    with app.app_context():
        db.session.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}";'))
        db.session.commit()

        @event.listens_for(db.engine, "connect")
        def _set_search_path(dbapi_connection, connection_record):
            with dbapi_connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{SCHEMA}", public;')

        db.session.execute(text(f'SET search_path TO "{SCHEMA}", public;'))
        db.session.commit()

        db.drop_all()
        db.session.commit()

        for ddl in ENUM_DDL:
            try:
                db.session.execute(text(ddl))
                db.session.commit()
            except Exception:
                db.session.rollback()


        db.create_all()
        db.session.commit()

    yield app


    with app.app_context():
        db.drop_all()
        db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def admin_user(app):
    """Seed one admin user for tests that need it."""
    from models import User  
    with app.app_context():
        existing = User.query.filter_by(email="admin@pets.com").first()
        if existing:
            return existing
        u = User(email="admin@pets.com", role="ADMIN")
        u.set_password("Admin123!")
        db.session.add(u)
        db.session.commit()
        return u


@pytest.fixture()
def sample_product(app):
    """Create (or fetch) a simple active product for cart/checkout tests."""
    from models import Product  
    with app.app_context():
        p = Product.query.filter_by(name="Test Food").first()
        if not p:
            p = Product(
                sku="TEST-FOOD-001",
                name="Test Food",
                description="Test item used in tests",
                price_cents=1500,
                stock=100,
                active=True,
            )
            db.session.add(p)
            db.session.commit()
        return p

def login(client, email: str, password: str) -> str:
    """Return a JWT access token for given credentials.
    If the user doesn't exist yet, register then login.
    """
    resp = client.post("/auth/login", json={"email": email, "password": password})
    if resp.status_code != 200:
        client.post("/auth/register", json={"email": email, "password": password})
        resp = client.post("/auth/login", json={"email": email, "password": password})
    data = resp.get_json() or {}
    token = data.get("access_token")
    assert token, f"Login failed: status={resp.status_code}, body={data}"
    return token


def auth_header_admin(client) -> dict:
    """Login as the seeded admin and return the Authorization header."""
    token = login(client, "admin@pets.com", "Admin123!")
    return {"Authorization": f"Bearer {token}"}