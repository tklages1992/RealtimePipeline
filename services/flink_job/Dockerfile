FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y netcat-openbsd bash \
 && pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# Start-Skript
ENTRYPOINT ["bash", "src/start.sh"]
