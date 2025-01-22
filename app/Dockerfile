FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/app

ENV PYTHONPATH=/code/app/

CMD ["python", "/code/app/main.py"]