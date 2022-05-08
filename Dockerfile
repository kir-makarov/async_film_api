FROM python:3.8.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY src/requirements.txt .
RUN pip install -r requirements.txt

ENV HOME=/src
RUN mkdir $HOME
WORKDIR $HOME

COPY src $HOME

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000