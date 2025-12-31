FROM python:3.10-bookworm

WORKDIR /app

COPY req_dock.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* 

RUN pip install -r req_dock.txt
RUN pip install jinja2

COPY . .

CMD ["python3","app.py"]


