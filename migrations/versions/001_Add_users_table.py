#coding=utf-8
from sqlalchemy import *
from sqlalchemy.sql.functions import current_timestamp


meta = MetaData()
users_table = Table(
    'users', meta,
    Column('id', Integer(), primary_key=True),
    Column('email', String(50), index=True, unique=True, nullable=False),
    Column('_password', String(32), nullable=False), #размер sha256 - 32 байта
    Column('created_at', DateTime(), default=current_timestamp(), nullable=False),
    Column('confirmed_at', DateTime()),
    #кол-во попыток входа с неправильным паролем
    Column('login_attempts', Integer(), default=0, nullable=False),
    Column('blocked_to', DateTime(), nullable=True),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users_table.create()
