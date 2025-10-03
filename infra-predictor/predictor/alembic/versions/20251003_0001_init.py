from alembic import op; import sqlalchemy as sa
revision = '20251003_0001_init'; down_revision = None; branch_labels=None; depends_on=None
def upgrade():
    op.execute(sa.schema.CreateSchema('raw')); op.execute(sa.schema.CreateSchema('curated'))
    op.create_table('matches',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('tournament', sa.String(128)), sa.Column('round', sa.String(32)), sa.Column('surface', sa.String(16)),
        sa.Column('player_a', sa.String(128), nullable=False), sa.Column('player_b', sa.String(128), nullable=False),
        sa.Column('winner', sa.String(128), nullable=False), sa.Column('score', sa.String(64)),
        sa.Column('rank_a', sa.Integer()), sa.Column('rank_b', sa.Integer()), sa.Column('source', sa.String(64), server_default='import'),
        schema='raw')
    op.create_table('odds',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('market_id', sa.String(64)), sa.Column('event_time', sa.DateTime()), sa.Column('selection', sa.String(128)),
        sa.Column('best_back', sa.Float()), sa.Column('best_lay', sa.Float()), sa.Column('implied_prob', sa.Float()), sa.Column('raw', sa.JSON()),
        schema='raw')
    op.create_table('live_points',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('match_id', sa.String(64)), sa.Column('ts', sa.DateTime()), sa.Column('server', sa.String(1)), sa.Column('point_winner', sa.String(1)),
        sa.Column('game_a', sa.Integer()), sa.Column('game_b', sa.Integer()), sa.Column('set_a', sa.Integer()), sa.Column('set_b', sa.Integer()), sa.Column('raw', sa.JSON()),
        schema='raw')
    op.create_table('features',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('match_key', sa.String(256)), sa.Column('player_a', sa.String(128)), sa.Column('player_b', sa.String(128)),
        sa.Column('features', sa.JSON()), sa.Column('label', sa.Integer()), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        schema='curated')
    op.create_table('predictions',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('match_key', sa.String(256)), sa.Column('p_pred', sa.Float()), sa.Column('y_true', sa.Integer()), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        schema='curated')
def downgrade():
    op.drop_table('predictions', schema='curated'); op.drop_table('features', schema='curated')
    op.drop_table('live_points', schema='raw'); op.drop_table('odds', schema='raw'); op.drop_table('matches', schema='raw')
    op.execute('DROP SCHEMA IF EXISTS curated CASCADE'); op.execute('DROP SCHEMA IF EXISTS raw CASCADE')
