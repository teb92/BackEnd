import pytest
from tests.conftest import login

@pytest.fixture()
def sample_product(app):
    """Create (or fetch) a simple active product and return its integer id.
    Returning an int avoids DetachedInstanceError from ORM session expiry.
    """
    from models import Product  
    from extensions import db
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
            db.session.flush()  # ensure p.id is populated
        product_id = p.id
        db.session.commit()
        return product_id

def test_cart_flow_create_add_checkout(client, admin_user, sample_product):
    token = login(client, "admin@pets.com", "Admin123!")
    headers = {"Authorization": f"Bearer {token}"}


    res = client.post("/carts", headers=headers)
    assert res.status_code in (200, 201)
    cart = res.get_json()
    cart_id = cart["id"] if "id" in cart else cart["cart"]["id"]


    product_id = sample_product


    res = client.post(
        f"/carts/{cart_id}/items",
        headers=headers,
        json={"product_id": product_id, "quantity": 2},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "cart" in data
    assert data["cart"]["status"] == "OPEN"


    res = client.post(
        f"/carts/{cart_id}/checkout",
        headers=headers,
        json={
            "billing_address": {
                "line1": "Calle 1, casa azul",
                "city": "San José",
                "region": "SJ",
                "postal_code": "10101",
                "country": "CR"
            },
            "payment": {"reference": "SINPE-TEST-123456"}
        },
    )
    assert res.status_code == 201
    payload = res.get_json()
    assert payload["order"]["status"] == "PAID"
    assert payload["cart"]["status"] == "CONVERTED"