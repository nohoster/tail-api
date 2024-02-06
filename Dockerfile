FROM python:3.11-alpine

WORKDIR /tail-api

COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN python-on-whales download-cli

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0
