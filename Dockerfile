FROM python:3.9.5-slim

RUN mkdir -p /usr/src/mio_api
WORKDIR /usr/src/mio_api

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY ./app ./app
COPY ./run_server.py .
COPY ./migarations ./migarations
COPY ./alembic.ini .
COPY ./clepsydra ./clepsydra