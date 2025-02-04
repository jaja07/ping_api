FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    pip install --no-cache-dir -r /code/requirements.txt && \
    apt-get clean 

COPY . /code/app

ENV PYTHONPATH=/code/app/

CMD ["python", "/code/app/main.py"]