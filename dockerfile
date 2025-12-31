FROM python:3.10-slim-bookworm

WORKDIR /app

COPY req_dock.txt .

RUN pip install -r req_dock.txt

COPY . .

CMD ["python3","app.py"]


