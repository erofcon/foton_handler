FROM python:3.10

RUN git clone https://github.com/erofcon/foton_handler.git /opt/foton_handler

RUN pip install --no-cache-dir --upgrade -r /opt/foton_handler/requirements.txt

WORKDIR /opt/foton_handler

EXPOSE 8000

RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]