FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django_app

COPY /hillel_messenger /django_app/hillel_messenger

RUN pip install --no-cache-dir -r /django_app/hillel_messenger/requirements.txt

WORKDIR /django_app/hillel_messenger

EXPOSE 8000

