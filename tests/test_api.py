from fastapi.testclient import TestClient
from bank_account.main import app

client = TestClient(app)

def test_create_account_endpoint():
    res = client.post("/accounts", json={"type": "CURRENT", "overdraft_limit": 300})
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "CURRENT"
    assert "id" in data

def test_deposit_and_withdraw_endpoints():
    # Créer un compte
    acc = client.post("/accounts", json={"type": "CURRENT"}).json()

    # Dépôt
    dep = client.post(f"/accounts/{acc['id']}/deposit", json={"amount": 200})
    assert dep.status_code == 200
    assert dep.json()["balance"] == 200

    # Retrait
    wd = client.post(f"/accounts/{acc['id']}/withdraw", json={"amount": 50})
    assert wd.status_code == 200
    assert wd.json()["balance"] == 150

def test_savings_account_cap_limit():
    acc = client.post("/accounts", json={"type": "SAVINGS", "deposit_cap": 1000}).json()
    dep1 = client.post(f"/accounts/{acc['id']}/deposit", json={"amount": 800})
    assert dep1.status_code == 200
    dep2 = client.post(f"/accounts/{acc['id']}/deposit", json={"amount": 300})
    assert dep2.status_code == 400  # dépasse le plafond

def test_get_statement():
    acc = client.post("/accounts", json={"type": "CURRENT"}).json()
    client.post(f"/accounts/{acc['id']}/deposit", json={"amount": 100})
    client.post(f"/accounts/{acc['id']}/withdraw", json={"amount": 50})
    stmt = client.get(f"/accounts/{acc['id']}/statement")
    assert stmt.status_code == 200
    data = stmt.json()
    assert "operations" in data
    assert len(data["operations"]) == 2
