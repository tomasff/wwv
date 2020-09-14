FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app

COPY ./web ./web
COPY ./repositories ./repositories

ENV STATIC_PATH /app/web/static

RUN pip install -r ./web/requirements.txt

COPY ./__init__.py .
COPY ./uwsgi.ini .