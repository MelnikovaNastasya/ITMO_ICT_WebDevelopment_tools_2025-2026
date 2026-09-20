FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY shared ./shared
COPY worker ./worker
CMD ["celery", "-A", "worker.celery_app:celery_app", "worker", "--loglevel=info", "--concurrency=2"]
