FROM python:3.8

WORKDIR /discord

COPY ./bot ./bot
COPY ./repositories ./repositories

RUN pip install -r ./bot/requirements.txt

CMD [ "python", "-m", "bot" ]