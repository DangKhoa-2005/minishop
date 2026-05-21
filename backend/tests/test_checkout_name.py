import requests

BASE = "http://host.docker.internal:5001"


def login(email, password):
    r = requests.post(f"{BASE}/api/auth/login", json={"email": email, "password": password})
    # Debug output for test runs
    print("[TEST-DEBUG] LOGIN STATUS:", r.status_code)
    try:
        print("[TEST-DEBUG] LOGIN BODY:", r.json())
    except Exception:
        print("[TEST-DEBUG] LOGIN BODY: <non-json response>")
    assert r.status_code == 200
    # API returns token under data.access_token
    return r.json()['data']['access_token']


def add_product_to_cart(token, product_id=1, quantity=1):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE}/api/cart/add", json={"product_id": product_id, "quantity": quantity}, headers=headers)
    assert r.status_code == 200
    return r.json()


def checkout(token, payload):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE}/api/orders/checkout", json=payload, headers=headers)
    return r


def test_checkout_uses_user_full_name_when_name_not_provided():
    """If client does not send `name`, backend should use user's full_name from profile"""
    token = login('customer@example.com', '123456')
    add_product_to_cart(token, product_id=1, quantity=1)

    payload = {
        "shipping_address": "123 Test Street",
        "phone": "0901234567"
    }

    r = checkout(token, payload)
    assert r.status_code == 201
    data = r.json()['data']
    assert data['customer_name'] == 'Nguyễn Văn A'


def test_checkout_uses_explicit_name_if_provided():
    """If client provides a `name`, it should be used as customer_name"""
    token = login('customer@example.com', '123456')
    add_product_to_cart(token, product_id=2, quantity=1)

    payload = {
        "name": "Huỳnh Đăng Khoa",
        "shipping_address": "456 Other Street",
        "phone": "0909876543"
    }

    r = checkout(token, payload)
    assert r.status_code == 201
    data = r.json()['data']
    assert data['customer_name'] == 'Huỳnh Đăng Khoa'
