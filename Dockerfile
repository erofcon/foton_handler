FROM python:3.10-slim-buster

RUN apt-get update
RUN apt install -y netcat
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install psycopg2-binary



COPY . /opt/foton_hundler

WORKDIR /opt/foton_hundler
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

