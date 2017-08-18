FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y npm
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN npm install srcds-rcon