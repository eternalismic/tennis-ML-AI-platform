FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_agent.py .
ENV KAFKA_BOOTSTRAP=kafka:9092
ENV ODDS_TOPIC=odds
ENV PRED_TOPIC=predictions
ENV MCP_EDGE=0.0
CMD ["python","mcp_agent.py"]
