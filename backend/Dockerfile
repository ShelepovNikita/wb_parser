FROM python:3.10

WORKDIR /parser_wb

COPY ./requirements.txt /parser_wb/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /parser_wb/requirements.txt

COPY ./app /parser_wb/app

# CMD for local start
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]