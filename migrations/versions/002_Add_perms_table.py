#coding=utf-8
from sqlalchemy import *


meta = MetaData()


#Права пользователя - это всего лишь строки с произвольным текстом,
#принадлежащие пользователю
perms_table = Table(
    'perms', meta,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column('permission', String(64), nullable=False),
    Index('idx_perms_user_id_permission', "user_id", "permission")
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('users', meta, autoload=True)
    perms_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    perms_table.create()
