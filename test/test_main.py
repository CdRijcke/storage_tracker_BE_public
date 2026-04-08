# import pytest
from uuid import UUID

from fastapi.testclient import TestClient


def test_read_product(client: TestClient):
    response = client.get("/product/peanutbutter", headers={"X-Token": "coneofsilence"})

    assert response.status_code == 200
    response_product = response.json()

    assert response_product["name"] == "peanutbutter"
    assert response_product["quantity"] == 2
    assert response_product["present"]
    assert UUID(response_product["id"], version=4)


def test_update_quantity(client: TestClient):
    response = client.get("/product/rice", headers={"X-Token": "coneofsilence"})

    assert response.status_code == 200
    response_product = response.json()

    assert response_product["name"] == "rice"
    assert response_product["quantity"] == 4

    client.patch("/update_product?product_name=rice&product_quantity=8")
    response_update = client.get("/product/rice", headers={"X-Token": "coneofsilence"})

    assert response_update.json()["quantity"] == 8


def test_auto_set_availability(client: TestClient):
    response = client.get("/product/rice", headers={"X-Token": "coneofsilence"})

    assert response.status_code == 200
    response_product = response.json()

    assert response_product["name"] == "rice"
    assert response_product["quantity"] == 4
    assert response_product["present"]

    client.patch("/update_product?product_name=rice&product_quantity=0")
    response_update = client.get("/product/rice", headers={"X-Token": "coneofsilence"})

    product_update = response_update.json()
    assert product_update["quantity"] == 0
    assert not product_update["present"]


def test_read_products(client: TestClient):
    response = client.get("/products")

    assert response.status_code == 200
    products = response.json()

    assert len(products) == 4
    names = [p["name"] for p in products]
    assert "peanutbutter" in names
    assert "rice" in names
    assert "coffee" in names
    assert "oat_milk" in names


def test_add_and_remove_product(client: TestClient):
    response = client.post("/add_product?product_name=pasta&product_quantity=3")
    assert response.status_code == 200

    response = client.get("/product/pasta")
    assert response.status_code == 200
    new_product = response.json()
    assert new_product["name"] == "pasta"
    assert new_product["quantity"] == 3
    assert new_product["present"]

    response = client.delete("/remove_product?product_name=pasta")
    assert response.status_code == 200

    response = client.get("/products")
    names = [p["name"] for p in response.json()]
    assert "pasta" not in names
