import os, glob, pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
def load_matches_to_db(path: str, db_url: str):
    engine = create_engine(db_url, future=True)
    def normalize(df: pd.DataFrame):
        cols = {c.lower(): c for c in df.columns}
        def pick(*names, default=None):
            for n in names:
                if n in cols: return df[cols[n]]
            return default
        return pd.DataFrame({
            "date": pd.to_datetime(pick("date","tourney_date", default=datetime.utcnow())),
            "tournament": pick("tournament","tourney_name","event"),
            "round": pick("round","match_round"),
            "surface": pick("surface"),
            "player_a": pick("player_a","winner_name","p1"),
            "player_b": pick("player_b","loser_name","p2"),
            "winner": pick("winner","winner_name","p1"),
            "score": pick("score","scoreline"),
            "rank_a": pd.to_numeric(pick("rank_a","winner_rank","p1_rank"), errors="coerce"),
            "rank_b": pd.to_numeric(pick("rank_b","loser_rank","p2_rank"), errors="coerce"),
            "source": "import"
        })
    files = [path] if os.path.isfile(path) else glob.glob(os.path.join(path, "*.csv"))
    for f in files:
        df = pd.read_csv(f)
        out = normalize(df)
        out.to_sql("matches", engine, schema="raw", if_exists="append", index=False, method="multi", chunksize=1000)
        print(f"[+] Loaded {len(out)} rows from {f}")
