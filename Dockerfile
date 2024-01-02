FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev postgresql-client

COPY requirements.txt ./

RUN apt-get install -y gcc libpq-dev


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8000


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "configs.wsgi:application"]