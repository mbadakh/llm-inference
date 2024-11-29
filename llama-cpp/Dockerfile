FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    #     ffmpeg \
    #     curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
EXPOSE 1234

ENTRYPOINT ["gunicorn"]
CMD ["--workers","1","--bind", "0.0.0.0:1234", "wsgi:app","--log-config", "logging.ini", "--timeout", "120"]
