import requests

BASE = "http://host.docker.internal:5001"


def test_health():
    r = requests.get(f"{BASE}/api/health")
    assert r.status_code == 200
    assert r.json().get('status') == 'healthy'
