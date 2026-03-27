from sqlmodel import Session, SQLModel
from storage_tracker.database.classes import Product
from storage_tracker.database.db import engine


product_list = [
    "oat_flakes",
    "peanutbutter",
    "oat_milk",
    "rice",
]


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for product_name in product_list:
            product = Product(name=product_name)
            session.add(product)

            session.commit()

            session.refresh(product)
