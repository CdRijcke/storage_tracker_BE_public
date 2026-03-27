from fastapi import FastAPI, Depends
from sqlmodel import Session
import uvicorn

from storage_tracker.database.classes import Product
from storage_tracker.database.db import get_product, update_product, engine

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def root():
    return {"message": "storage tracker 3000"}


@app.get("/product/{product_name}", response_model=Product)
def read_product(product_name: str, session: Session = Depends(get_session)):
    product_db = get_product(session, product_name)

    return product_db


@app.patch("/update_product", response_model=Product)
def update_product_quantity(product_name: str, product_quantity: int, session: Session = Depends(get_session)):
    product_db = get_product(session, product_name)
    product_db = update_product(session, product_db, product_quantity)

    return product_db  # TODO: check why no response body


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload = True,
        reload_dirs = ["html_files"],
        port=8000,
        ssl_keyfile="",
        ssl_certfile=""
    )
