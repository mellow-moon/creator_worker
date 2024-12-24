FROM python:3.11-slim

WORKDIR /worker_app

COPY worker/requirements.txt /worker_app/requirements.txt

RUN apt-get update
RUN apt-get install gcc python3-dev libpq-dev -y

RUN pip install --no-cache-dir -r requirements.txt

COPY worker /worker_app