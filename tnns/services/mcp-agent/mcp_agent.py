import json, os, time
from kafka import KafkaConsumer, KafkaProducer

bootstrap = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
topic_in = os.getenv("ODDS_TOPIC", "odds")
topic_out = os.getenv("PRED_TOPIC", "predictions")
group_id = os.getenv("GROUP_ID", "mcp-agent")
edge = float(os.getenv("MCP_EDGE", "0.0"))

def norm_probs(p1, p2):
    s = p1 + p2
    return (p1/s, p2/s) if s > 0 else (0.5, 0.5)

def main():
    consumer = KafkaConsumer(
        topic_in,
        bootstrap_servers=bootstrap,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=group_id,
    )
    producer = KafkaProducer(
        bootstrap_servers=bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"[MCP] Consuming from {topic_in}, producing to {topic_out}, edge={edge}")
    for msg in consumer:
        data = msg.value or {}
        p1o = float(data.get("player1_odds") or 0)
        p2o = float(data.get("player2_odds") or 0)
        if p1o <= 1.0 or p2o <= 1.0:
            continue
        mp1 = 1.0 / p1o
        mp2 = 1.0 / p2o
        mp1, mp2 = norm_probs(mp1, mp2)
        model_p1 = min(max(mp1 + edge, 0.0), 1.0)
        model_p2 = 1.0 - model_p1
        out = {
            "provider": data.get("provider"),
            "match": data.get("match","unknown"),
            "player1": data.get("player1","PlayerA"),
            "player2": data.get("player2","PlayerB"),
            "p1_odds": p1o,
            "p2_odds": p2o,
            "market_prob_a": mp1,
            "market_prob_b": mp2,
            "model_prob_a": model_p1,
            "model_prob_b": model_p2,
            "betfair_market_id": data.get("betfair_market_id"),
            "player1_selection_id": data.get("player1_selection_id"),
            "player2_selection_id": data.get("player2_selection_id"),
            "ts": time.time()
        }
        producer.send(topic_out, out)

if __name__ == "__main__":
    main()
