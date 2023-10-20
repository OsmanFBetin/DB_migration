FROM python:3.11.4-slim

WORKDIR /BD_migration

COPY . /BD_migration

RUN pip install -r requirements.txt 

CMD uvicorn main:app --reload --host=0.0.0.0