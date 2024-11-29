FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 1234

ENTRYPOINT ["gunicorn"]
CMD ["--workers","7","--bind", "0.0.0.0:1234", "wsgi:app","--log-config", "logging.ini", "--timeout", "120"]
