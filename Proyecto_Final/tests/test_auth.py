# tests/test_auth.py
def test_register_and_login(client):
    # Register
    res = client.post("/auth/register", json={
        "email": "user1@pets.com",
        "password": "Secret123!"
    })
    assert res.status_code in (200, 201)

    # Login
    res = client.post("/auth/login", json={
        "email": "user1@pets.com",
        "password": "Secret123!"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data

    # Authenticated user info
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    res = client.get("/auth/me", headers=headers)
    assert res.status_code == 200
    me = res.get_json()
    assert "user_id" in me