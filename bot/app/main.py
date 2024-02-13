"""Модуль содержит в себе функции для телеграмм бота."""

import time
import json
import os

from fastapi import FastAPI
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

URL = "https://api.telegram.org/"
TOKEN = os.environ.get("TOKEN")
TOKEN = f"bot{TOKEN}"


def pretty_answer(data) -> str:
    """Преобразование ответа в построчное сообщение для телеграма."""

    nm_id = data.get("nm_id")
    name = data.get("name")
    brand = data.get("brand")
    brand_id = data.get("brand_id")
    site_brand_id = data.get("site_brand_id")
    supplier_id = data.get("supplier_id")
    sale = data.get("sale")
    price = data.get("price")
    sale_price = data.get("sale_price")
    rating = data.get("rating")
    feedbacks = data.get("feedbacks")
    colors = data.get("colors")
    quantity = data.get("quantity")

    detail = data.get("detail")

    if nm_id:
        answer = (
            f"nm_id: {nm_id} \n"
            f"name: {name} \n"
            f"brand: {brand} \n"
            f"brand_id: {brand_id} \n"
            f"site_brand_id: {site_brand_id} \n"
            f"supplier_id: {supplier_id} \n"
            f"sale: {sale} \n"
            f"price: {price} \n"
            f"sale_price: {sale_price} \n"
            f"rating: {rating} \n"
            f"feedbacks: {feedbacks} \n"
            f"colors: {colors} \n"
            f"quantity: {quantity} \n"
        )
    elif detail:
        answer = f"detail: {detail}"
    else:
        answer = "Some error"

    return answer


def get_updates(offset=0) -> str:
    "Запрос на получение обнолвений на свервере телеграма."
    result = requests.get(f"{URL}{TOKEN}/getUpdates?offset={offset}").json()
    return result.get("result")


def send_message(chat_id, text):
    """Запрос на сервер телеграм с ответом пользователю."""
    requests.get(f"{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")


def check_message(chat_id, message):
    """Обработчик сообщения пользователя."""
    if message == "/help":
        return send_message(
            chat_id,
            "Доступные команды:\n "
            "/add - Добавить товар в БД по nm_id\n "
            "/products - Посмотреть все товары из БД\n "
            "/get_product - Посмотреть товар в БД по nm_id\n "
            "/delete_product - Удалить товар из БД по nm_id.",
        )
    if message == "/add":
        send_message(chat_id, "Ожидание ввода nm_id ....")
        update_id = 0
        if _update := get_updates():
            update_id = _update[-1]["update_id"]
        while True:
            time.sleep(2)
            messages = get_updates(update_id)
            for message in messages:
                if update_id < message["update_id"]:
                    update_id = message["update_id"]
                    response = requests.post(
                        "http://parser_wb_app/products/",
                        json={"nm_id": message.get("message").get("text")},
                    )
                    return send_message(
                        chat_id, pretty_answer(json.loads(response.text))
                    )

    elif message == "/products":
        response = requests.get(
            "http://parser_wb_app/products/",
        )
        products = json.loads(response.text)
        if len(products) == 0:
            send_message(chat_id, "В базе данных нет добавленных товаров.")
        else:
            for product in products:
                send_message(chat_id, pretty_answer(product))
        return
    elif message == "/get_product":
        send_message(chat_id, "Ожидание ввода nm_id ....")
        update_id = 0
        if _update := get_updates():
            update_id = _update[-1]["update_id"]
        while True:
            time.sleep(2)
            messages = get_updates(update_id)
            for message in messages:
                if update_id < message["update_id"]:
                    update_id = message["update_id"]
                    nm_id = message.get("message").get("text")
                    response = requests.get(
                        f"http://parser_wb_app/products/{nm_id}"
                    )
                    return send_message(
                        chat_id, pretty_answer(json.loads(response.text))
                    )
    if message == "/delete_product":
        send_message(chat_id, "Ожидание ввода nm_id ....")
        update_id = 0
        if _update := get_updates():
            update_id = _update[-1]["update_id"]
        while True:
            time.sleep(2)
            messages = get_updates(update_id)
            for message in messages:
                if update_id < message["update_id"]:
                    update_id = message["update_id"]
                    nm_id = message.get("message").get("text")
                    response = requests.delete(
                        f"http://parser_wb_app/products/{nm_id}"
                    )
                    return send_message(
                        chat_id, pretty_answer(json.loads(response.text))
                    )


@app.on_event("startup")
async def on_startup():
    """Запуск проверки обновлений бесконечным циклом."""
    update_id = 0
    if _update := get_updates():
        update_id = _update[-1]["update_id"]
    while True:
        time.sleep(2)
        messages = get_updates(update_id)
        for message in messages:
            if update_id < message["update_id"]:
                update_id = message["update_id"]
                check_message(
                    message["message"]["chat"]["id"],
                    message["message"]["text"],
                )
