FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
        imagemagick \
        ca-certificates \
        ghostscript \ 
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN mkdir -p images/input images/output && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

