"""Главный файл для запуска приложения."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, utils
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Подключение к БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=schemas.Product)
def parse_product_to_db(
    product: schemas.ProductBase, db: Session = Depends(get_db)
) -> models.Product:
    """Эндпоинт на создание записи в БД о товаре."""
    db_product = crud.get_product_by_nm_id(db, nm_id=product.nm_id)
    # Проверяем наличие товара в базе данных.
    if db_product:
        raise HTTPException(
            status_code=400, detail="Product already in database"
        )
    # Запрос на сайт для получения товара
    try:
        product_json = utils.request_to_wb(product.nm_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=error)
    # Если неправильный nm_id
    if product_json.get("detail") == "product not found":
        raise HTTPException(status_code=404, detail="product not found")
    else:
        quantity = utils.request_to_wb_get_quantity(product.nm_id)
        db_product = utils.parse_json(product_json, quantity)
        return crud.create_product(db, db_product)


@app.get("/products/", response_model=list[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    """Эндпоинт на получение всех товаров из БД."""
    return crud.get_products(db)


@app.get("/products/{nm_id}", response_model=schemas.Product)
def get_product_by_nm_id(
    nm_id: int, db: Session = Depends(get_db)
) -> models.Product:
    """Эндпоинт на получение товара из БД по nm_id."""
    db_product = crud.get_product_by_nm_id(db, nm_id=nm_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.delete("/products/{nm_id}/")
def delete_product_by_nm_id(nm_id: int, db: Session = Depends(get_db)):
    """Эндпоинт на удаление товара из БД по nm_id."""
    db_product = crud.get_product_by_nm_id(db, nm_id=nm_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.delete_product(db, db_product=db_product)
