FROM python:3.10

WORKDIR /parser_wb_bot

COPY ./requirements.txt /parser_wb_bot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /parser_wb_bot/requirements.txt

COPY ./app /parser_wb_bot/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]