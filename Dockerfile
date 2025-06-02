FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
