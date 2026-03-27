from sqlmodel import Session, create_engine

from storage_tracker.database.classes import Product


sqlite_file_name = "db/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)


# TODO: add engine as depency to function
def get_product(session: Session, product_name: str) -> Product:
    product_db = session.get(Product, product_name)

    if not product_db:
        raise Exception("product not found")

    return product_db


def update_product(session: Session, product_db: Product, quantity: int) -> Product:
    if quantity < 0:
        raise Exception("quantity cannot be negative")

    product_db.quantity = quantity
    product_db.set_presence()

    session.add(product_db)
    session.commit()

    return product_db
