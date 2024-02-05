FROM python:3.11-alpine

WORKDIR /tail-api

COPY main.py requirements.txt ./

RUN pip install -r requirements.txt

RUN python-on-whales download-cli

CMD uvicorn main:app --host 0.0.0.0
