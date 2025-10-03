FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY odds_ingest.py .
ENV KAFKA_BOOTSTRAP=kafka:9092
ENV ODDS_TOPIC=odds
CMD ["python","odds_ingest.py"]
