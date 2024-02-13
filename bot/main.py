import requests
import time
from fastapi import Depends, FastAPI, HTTPException
import json

app = FastAPI()

URL = "https://api.telegram.org/"
TOKEN = ""


def get_updates(offset=0):
    result = requests.get(f"{URL}{TOKEN}/getUpdates?offset={offset}").json()
    # with open("123.json", "w") as f:
    #     json.dump((result["result"]), f, ensure_ascii=False, indent=4)
    return result["result"]


def send_message(chat_id, text):
    requests.get(f"{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}")


def check_message(chat_id, message):
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

                    return send_message(chat_id, "Доступные команды:\n ")

    if message == "/products":
        send_message(chat_id, "Продукты")
    if message == "/get_product":
        send_message(chat_id, "Ожидание ввода nm_id ....")
    if message == "/delete_product":
        send_message(chat_id, "Ожидание ввода nm_id ....")


@app.on_event("startup")
async def on_startup():
    update_id = 0
    if _update := get_updates():
        update_id = _update[-1]["update_id"]
    while True:
        time.sleep(2)
        messages = get_updates(update_id)  # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message["update_id"]:
                update_id = message[
                    "update_id"
                ]  # Присваиваем ID последнего отправленного сообщения боту
                # Отвечаем тому кто прислал сообщение боту
                check_message(
                    message["message"]["chat"]["id"],
                    message["message"]["text"],
                )
