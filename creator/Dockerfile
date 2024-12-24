FROM python:3.11-slim

WORKDIR /creator_app

COPY creator/requirements.txt /creator_app/requirements.txt

RUN apt-get update
RUN apt-get install gcc python3-dev libpq-dev -y

RUN pip install --no-cache-dir -r requirements.txt

COPY creator /creator_app

EXPOSE 8000