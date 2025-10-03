
# Tennis MCP — Autonomous Betting Platform

Welcome! This site explains **what the platform does**, **how it works**, and **how to run it**.

> **Goal:** Use machine learning to estimate win probabilities, compare them to market odds, and **bet only when there is value** — automatically and safely.

**At a glance:**

- Predict win probabilities for tennis matches (model or baseline).
- Compute **fair odds** and **edge** vs market prices.
- Place bets only if edge ≥ threshold; size stakes via capped Kelly.
- Observe decisions and performance via Prometheus + Grafana.
- Roll out gradually: backtest → simulate (shadow) → real money.

For a story-like explanation for different audiences, see **[MCP & Strategy](mcp.md)**.
