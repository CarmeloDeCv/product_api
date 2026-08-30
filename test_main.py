from fastapi.testclient import TestClient
from main import app

client= TestClient(app)

def test_home():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={"message": "It works"}

def test_create_and_get_product():
    client.post("/register", data={"username":"melons", "password":"melons"})

    login_response = client.post("/login", data={"username":"melons", "password":"melons"})
    token=login_response.json()["access_token"]

    headers= {"Authorization": f"Bearer {token}"}

    response=client.post("/products", json={"name": "testpizza", "price": 9.99, "in_stock":True},headers=headers)
    assert response.status_code==200
    data=response.json()
    assert data["name"] == "testpizza"
    product_id= data["id"]

    get_response = client.get(f"/products/{product_id}", headers=headers)
    assert get_response.status_code==200
    assert get_response.json()["name"]=="testpizza"