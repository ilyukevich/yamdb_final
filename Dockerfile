FROM python:3.8.5

#FROM ilyukevich/yamdb:v1

RUN mkdir /code

#COPY requirements.txt /code

COPY . /code

#RUN apt update && apt upgrade

RUN pip install -r /code/requirements.txt
    
CMD python manage.py makemigrations && \
    python manage.py makemigrations api && \
    python manage.py migrate && \
    python manage.py collectstatic


#CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
