from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime, BigInteger, JSON, text

metadata = MetaData(schema="raw")
matches = Table("matches", metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("date", DateTime, nullable=False),
    Column("tournament", String(128)), Column("round", String(32)), Column("surface", String(16)),
    Column("player_a", String(128), nullable=False), Column("player_b", String(128), nullable=False),
    Column("winner", String(128), nullable=False), Column("score", String(64)),
    Column("rank_a", Integer), Column("rank_b", Integer), Column("source", String(64))
)
odds = Table("odds", metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("market_id", String(64)), Column("event_time", DateTime), Column("selection", String(128)),
    Column("best_back", Float), Column("best_lay", Float), Column("implied_prob", Float), Column("raw", JSON),
)
live_points = Table("live_points", metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("match_id", String(64)), Column("ts", DateTime), Column("server", String(1)), Column("point_winner", String(1)),
    Column("game_a", Integer), Column("game_b", Integer), Column("set_a", Integer), Column("set_b", Integer), Column("raw", JSON),
)

cur_meta = MetaData(schema="curated")
features = Table("features", cur_meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("match_key", String(256)), Column("player_a", String(128)), Column("player_b", String(128)),
    Column("features", JSON), Column("label", Integer), Column("created_at", DateTime, server_default=text("now()"))
)
predictions = Table("predictions", cur_meta,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("match_key", String(256)), Column("p_pred", Float), Column("y_true", Integer), Column("created_at", DateTime, server_default=text("now()"))
)
