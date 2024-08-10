FROM python:3.11.8-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean


WORKDIR /django-book


COPY . /django-book/


RUN pip install -r requirements.txt


COPY .env /django-book/.env




CMD ["python", "manage.py", "runserver"]