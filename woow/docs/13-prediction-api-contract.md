
# Prediction API Contract

**POST** `/predict` with `{ "player_a": "...", "player_b": "...", "score": "optional" }`  
**Response** `{ "prob_a": 0.62, "prob_b": 0.38 }` (will be normalized).  
If the API is down, MCP falls back to market‑implied probabilities.

Metrics & calls should be cached per match to reduce load.
