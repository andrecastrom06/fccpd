FROM python:3.11-slim

WORKDIR /app

COPY gateway.py .

RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install flask requests

CMD ["python", "gateway.py"]