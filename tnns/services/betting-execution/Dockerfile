FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY betting_exec.py .
ENV KAFKA_BOOTSTRAP=kafka:9092
ENV PRED_TOPIC=predictions
ENV EDGE_THRESHOLD=0.05
CMD ["python","betting_exec.py"]
