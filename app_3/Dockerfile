FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt


RUN apt-get update && \
    apt install -y ffmpeg && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . /code/app


ENV PYTHONPATH=/code/app/

CMD ["python", "/code/app/main.py"]