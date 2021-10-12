FROM python:3.8

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY posts.csv config.py main.py db_init.py start.sh ./
RUN chmod +x start.sh

EXPOSE 5000