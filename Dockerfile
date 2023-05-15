FROM python:3.8

WORKDIR /bacana-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./app/static ./app/static
COPY ./app/client_store ./app/client_store
COPY ./app/credentials ./app/credentials

CMD ["python", "./app/main.py"]