import sqlalchemy as SQL


metadata = SQL.MetaData()


devices = SQL.Table(
    "devices",
    metadata,
    SQL.Column('id', SQL.Integer, primary_key=True),
    SQL.Column('name', SQL.String),
    SQL.Column('active', SQL.Boolean, is_nullable=True),
    SQL.Column('connected', SQL.Boolean),
)

measurements = SQL.Table(
    "measurements",
    metadata,
    SQL.Column('id', SQL.Integer, primary_key=True),
    SQL.Column('created_at', SQL.DateTime),
    SQL.Column('device_id', SQL.Integer),
    SQL.Column('reading', SQL.Float),
)
