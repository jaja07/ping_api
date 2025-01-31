FROM python:3.12-slim

WORKDIR /code

COPY requirements_2.txt /code/requirements_2.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf && \
    pip install --no-cache-dir -r requirements_2.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . /code/app_2

ENV PYTHONPATH=/code/app_2/

CMD ["python", "/code/app_2/main.py"]