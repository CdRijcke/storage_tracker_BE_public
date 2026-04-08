import os
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, create_engine, select

from storage_tracker.database.classes import Product


sqlite_file_name = "db/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

_echo = os.environ.get("ENVIRONMENT") != "production"
engine = create_engine(sqlite_url, echo=_echo)


def get_product(session: Session, product_name: str) -> Product:
    product_db = session.get(Product, product_name)

    if not product_db:
        raise HTTPException(status_code=404, detail=f"product '{product_name}' not found")

    return product_db


def get_all_products(session: Session) -> List[Product]:
    statement = select(Product)
    products_db = session.exec(statement)

    return list(products_db.all())


def update_product(session: Session, product_db: Product, quantity: int) -> Product:
    if quantity < 0:
        raise HTTPException(status_code=400, detail="quantity cannot be negative")

    product_db.quantity = quantity
    product_db.set_presence()

    session.add(product_db)
    session.commit()

    return product_db


def dev__add_product(session: Session, product_name: str, quantity: int) -> Product:
    product_db = session.get(Product, product_name)

    if product_db:
        raise HTTPException(status_code=409, detail=f"product '{product_name}' already exists")

    product_db = Product(name=product_name,
                         quantity=quantity)

    product_db.set_presence()

    session.add(product_db)
    session.commit()

    return product_db


def dev__remove_product(session: Session, product_name: str):
    product_db = session.get(Product, product_name)

    if not product_db:
        raise HTTPException(status_code=404, detail=f"product '{product_name}' not found")

    session.delete(product_db)
    session.commit()


def dev__remove_all_products(session: Session):
    stmt = select(Product)
    products_db = session.exec(stmt)

    for product_db in products_db.all():
        session.delete(product_db)

    session.commit()
