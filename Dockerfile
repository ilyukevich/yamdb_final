#FROM python:3.8.5

FROM ilyukevich/yamdb:v1

RUN mkdir /code

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt && \
    python manage.py makemigrations && \
    python manage.py makemigrations api && \
    python manage.py migrate


CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
