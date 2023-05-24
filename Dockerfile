FROM python:3.8

WORKDIR /bacana-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./app/static ./app/static
COPY ./app/static/css ./app/static/css
COPY ./app/static/documents ./app/static/documents
COPY ./app/static/images ./app/static/images
COPY ./app/static/js ./app/static/js
COPY ./app/client_store ./app/client_store
COPY ./app/credentials ./app/credentials

CMD ["python", "./app/main.py"]