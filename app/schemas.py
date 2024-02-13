"""Модуль для хранения схем для валидации."""

from pydantic import BaseModel


class ProductBase(BaseModel):
    nm_id: int


class Product(ProductBase):

    name: str
    brand: str
    brand_id: int
    site_brand_id: int
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: int
    feedbacks: int
    colors: str
    quantity: int | None

    class Config:
        orm_mode = True
