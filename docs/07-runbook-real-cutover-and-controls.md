
# Cutover to REAL (small stakes)

- Switch `agent.mode=REAL`, provide Betfair credentials and (optionally) client cert for **non‑interactive login** (`certlogin`). citeturn0search2
- Expect **in‑play bet delays** (1–12s typical); keep Kelly cap low initially. citeturn0search19
- Watch `pnl_total`, `roi_total`, `pending_exposure`, `daily_pnl`. Add Slack/email routes in Alertmanager.
