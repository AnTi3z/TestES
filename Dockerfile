FROM python:3.8-alpine

RUN adduser -D tester

WORKDIR /home/tester

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/python db_init.py

COPY app app
COPY main.py ./

RUN chown -R tester:tester ./
USER tester

EXPOSE 5000