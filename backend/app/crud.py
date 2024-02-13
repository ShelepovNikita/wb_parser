"""Модуль содержит в себе функции для работы с базой данных."""

from sqlalchemy.orm import Session

from app import models, schemas


def delete_product(db: Session, db_product: schemas.Product) -> dict:
    """Удаление товара."""
    db.delete(db_product)
    db.commit()
    return {"detail": "Success"}


def get_product_by_nm_id(db: Session, nm_id: int):
    """Получение товара по nm_id."""
    return (
        db.query(models.Product).filter(models.Product.nm_id == nm_id).first()
    )


def get_products(db: Session):
    """Получение всех товаров."""
    return db.query(models.Product).all()


def create_product(db: Session, db_product: schemas.Product):
    """Создание товара."""
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
