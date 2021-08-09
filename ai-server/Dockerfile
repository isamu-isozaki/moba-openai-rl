FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y libffi-dev python3-dev gcc
RUN apt-get install -y python-psycopg2
RUN pip3 install --upgrade pip \
  && pip3 install --upgrade pipenv \
  && pip3 install --upgrade -r /app/requirements.txt

ENV PYTHONUNBUFFERED=1
COPY . /app
RUN pip3 install -e ./gym_env
RUN pip3 install -e ./stable-baselines3