FROM python:alpine3.10

WORKDIR /parser_wb_bot

COPY ./requirements.txt /parser_wb_bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /parser_wb_bot/requirements.txt

COPY ./app /parser_wb_bot/app

# CMD for local start
# CMD ["python", "app/main.py" ]