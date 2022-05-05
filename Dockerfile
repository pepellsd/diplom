FROM python:3.9.5-slim

RUN mkdir -p /usr/src/application
WORKDIR /usr/src/application

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000