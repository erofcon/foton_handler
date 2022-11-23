FROM python:3.10-slim-buster

RUN apt-get update
RUN apt-get install -y git
RUN apt install -y netcat
RUN apt-get install -y git
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install psycopg2-binary


RUN git clone https://github.com/erofcon/foton_handler.git /opt/foton_handler/

WORKDIR /opt/foton_handler/
RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

