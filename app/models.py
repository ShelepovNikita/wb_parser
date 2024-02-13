"""Модуль для хранения моделей для базы данных."""

from sqlalchemy import Column, Integer, String

from app.database import Base


class Product(Base):
    """Модель товара."""

    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    nm_id: int = Column(Integer, unique=True)
    name: str = Column(String)
    brand: str = Column(String)
    brand_id: int = Column(Integer)
    site_brand_id: int = Column(Integer)
    supplier_id: int = Column(Integer)
    sale: int = Column(Integer)
    price: int = Column(Integer)
    sale_price: int = Column(Integer)
    rating: int = Column(Integer)
    feedbacks: int = Column(Integer)
    colors: str = Column(String)
    quantity: int = Column(Integer, nullable=True)
