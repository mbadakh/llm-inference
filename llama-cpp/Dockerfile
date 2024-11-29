FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    #     ffmpeg \
    #     curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
RUN pip install --no-cache-dir -r requirements.txt


COPY ./Meta-Llama-3-8B-Instruct.Q2_K.gguf .
COPY . .
EXPOSE 1234

ENTRYPOINT ["gunicorn"]
CMD ["--workers","1","--bind", "0.0.0.0:1234", "wsgi:app", "--timeout", "120"]
