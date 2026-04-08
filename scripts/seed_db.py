from sqlmodel import Session, create_engine, SQLModel
from storage_tracker.database.classes import Product
from storage_tracker.database.db import sqlite_url

products = [
    ("peanutbutter", 2),
    ("rice", 4),
    ("coffee", 0),
    ("oat_milk", 1),
]

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    for name, quantity in products:
        existing = session.get(Product, name)
        if not existing:
            product = Product(name=name, quantity=quantity)
            product.set_presence()
            session.add(product)
    session.commit()

print("Database seeded.")
