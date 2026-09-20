FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY shared ./shared
COPY parser_service ./parser_service
CMD ["uvicorn", "parser_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
