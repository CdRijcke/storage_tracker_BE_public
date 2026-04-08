from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str = Field(index=True, primary_key=True)
    quantity: int | None = Field(default=None, index=True)
    present: Optional[bool] = False  # NOTE: cant be auto updated yet: https://github.com/fastapi/sqlmodel/issues/453

    def set_presence(self):
        if self.quantity is not None:
            self.present = self.quantity > 0
        else:
            self.present = None


class Product(ProductBase, table=True):
    id: UUID | None = Field(default_factory=uuid4)
