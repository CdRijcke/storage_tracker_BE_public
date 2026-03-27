import pytest
from sqlalchemy import delete
from sqlmodel import SQLModel, Session, create_engine

from storage_tracker.database.classes import Product


@pytest.fixture(name="session", scope='session')
def session():
    test_sqlite_file_name = "db/test_database.db"
    test_sqlite_url = f"sqlite:///{test_sqlite_file_name}"
    engine = create_engine(test_sqlite_url, echo=True)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(scope='session')
def test_product() -> Product:
    product = Product(name="peanutbutter", quantity=2)
    product.set_presence()

    return product


@pytest.fixture(autouse=True)
def populate_test_db(session: Session, test_product: Product):
    stmt = delete(Product).where(Product.name == test_product.name)
    session.execute(stmt)
    session.commit()
    session.flush()

    session.add(test_product)
    session.commit()
