import logging
import os
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from storage_tracker.database.classes import Product
from storage_tracker.database.db import (dev__add_product,
                                         dev__remove_all_products,
                                         dev__remove_product,
                                         get_all_products,
                                         get_product,
                                         update_product,
                                         engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("%s %s -> %d %s", request.method, request.url.path, exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

_domain = os.environ.get("CORS_DOMAIN", "")
origins = [f"https://{_domain}"] if _domain else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_api_key = os.environ.get("API_KEY", "")


def require_api_key(x_api_key: str = Header(...)):
    if not _api_key or x_api_key != _api_key:
        raise HTTPException(status_code=403, detail="forbidden")


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def root():
    return {"message": "storage tracker 2030"}


@app.get("/product/{product_name}", response_model=Product)
def read_product(product_name: str, session: Session = Depends(get_session)):
    logger.info("GET /product/%s", product_name)
    product_db = get_product(session, product_name)

    return product_db


@app.get("/products", response_model=List[Product])
def read_products(session: Session = Depends(get_session)):
    logger.info("GET /products")
    products_db = get_all_products(session)

    return products_db


@app.patch("/update_product", response_model=Product)
def update_product_quantity(product_name: str, product_quantity: int, session: Session = Depends(get_session)):
    logger.info("PATCH /update_product name=%s quantity=%d", product_name, product_quantity)
    product_db = get_product(session, product_name)
    product_db = update_product(session, product_db, product_quantity)

    return product_db  # TODO: check why no response body


@app.post("/add_product", response_model=Product, dependencies=[Depends(require_api_key)])
def add_new_product(product_name: str, product_quantity: int = 0, session: Session = Depends(get_session)):
    logger.info("POST /add_product name=%s quantity=%d", product_name, product_quantity)
    product_db = dev__add_product(session, product_name, product_quantity)

    return product_db


@app.delete("/remove_product", dependencies=[Depends(require_api_key)])
def remove_product(product_name: str, session: Session = Depends(get_session)):
    logger.info("DELETE /remove_product name=%s", product_name)
    dev__remove_product(session, product_name)

    return {"message": f"{product_name} succesfully removed from DB"}


@app.delete("/delete_all_products", dependencies=[Depends(require_api_key)])
def remove_all_products(session: Session = Depends(get_session)):
    logger.warning("DELETE /delete_all_products")
    dev__remove_all_products(session)

    return {"message": "all product are removed from DB"}
