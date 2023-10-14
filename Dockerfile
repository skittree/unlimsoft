FROM python:3.8-slim as backend
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .