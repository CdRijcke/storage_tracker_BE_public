
from typing import List

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

from storage_tracker.database.classes import Product

from storage_tracker.main import app, get_session, require_api_key


@pytest.fixture(name="session", scope='session')
def session_fixture():
    engine = create_engine("sqlite:///:memory:",
                           echo=True,
                           connect_args={"check_same_thread": False},
                           poolclass=StaticPool)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client", scope="session")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[require_api_key] = lambda: None

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def test_products() -> List[Product]:

    products: List[Product] = []

    products_set_list: List[tuple[str, int]] = [
        ("peanutbutter", 2),
        ("rice", 4),
        ("coffee", 0),
        ("oat_milk", 1)
    ]

    for product_set in products_set_list:
        product = Product(name=product_set[0], quantity=product_set[1])
        product.set_presence()

        products.append(product)

    return products


@pytest.fixture(autouse=True)
def populate_test_db(client: TestClient, test_products: List[Product]):
    client.delete("/delete_all_products")

    for test_product in test_products:
        client.post(f"/add_product?product_name={test_product.name}&product_quantity={test_product.quantity}",
                    headers={"X-Token": "coneofsilence"})
