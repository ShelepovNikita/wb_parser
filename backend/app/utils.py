"""Модуль для хранения дополнительных функций."""

import json

import requests
from app import models


def get_colors_names(color) -> str:
    """Получение названий цветов из словаря с массивами."""
    return color.get("name")


def request_to_wb(nm_id) -> json:
    """Запрос к ВБ на получение карточки товара."""
    params: dict = {
        "curr": "rub",
        "nm": nm_id,
    }

    response = requests.get(
        "https://card.wb.ru/cards/v1/detail", params=params
    )
    data = json.loads(response.text)
    if len(data.get("data").get("products")) != 0:
        return json.loads(response.text)
    else:
        return {"detail": "product not found"}


def request_to_wb_get_quantity(nm_id) -> int | None:
    """Запрос к ВБ на получение количества на остаток."""
    # Это костыль, но рабочий))
    basket_num: int = 20
    vol: str = str(nm_id)[0:4]
    part: str = str(nm_id)[0:6]
    for i in range(basket_num):
        url = (
            f"https://basket-{i}.wbbasket.ru/vol{vol}/part{part}/{nm_id}/"
            "info/ru/card.json"
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except Exception as error:
            print(error)
    ids = json.loads(response.text).get("colors")
    result = ""
    for i in range(len(ids)):
        result += str(ids[i])
        if i != len(ids) - 1:
            result += ";"
    try:
        response = requests.get(
            (
                f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&"
                f"dest=-1257786&spp=30&nm={result}"
            )
        )
    except Exception:
        return None
    products = json.loads(response.text).get("data").get("products")
    for product in products:
        if str(product.get("id")) == str(nm_id):
            if len(product.get("sizes")[0].get("stocks")) != 0:
                quantity = product.get("sizes")[0].get("stocks")[0].get("qty")
                break
            else:
                quantity = None
    return quantity


def parse_json(product_json, quantity=None) -> models.Product:
    """Разбор JSON ответа по атрибутам."""

    colors: list = map(
        get_colors_names,
        product_json.get("data").get("products")[0].get("colors"),
    )

    product = models.Product(
        nm_id=product_json.get("data").get("products")[0].get("id"),
        name=product_json.get("data").get("products")[0].get("name"),
        brand=product_json.get("data").get("products")[0].get("brand"),
        brand_id=product_json.get("data").get("products")[0].get("brandId"),
        site_brand_id=product_json.get("data")
        .get("products")[0]
        .get("siteBrandId"),
        supplier_id=product_json.get("data")
        .get("products")[0]
        .get("supplierId"),
        sale=product_json.get("data").get("products")[0].get("sale"),
        price=product_json.get("data").get("products")[0].get("priceU"),
        sale_price=product_json.get("data")
        .get("products")[0]
        .get("salePriceU"),
        rating=product_json.get("data").get("products")[0].get("rating"),
        feedbacks=product_json.get("data").get("products")[0].get("feedbacks"),
        colors=", ".join(colors),
        quantity=quantity,
    )
    return product
