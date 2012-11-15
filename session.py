from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Db = create_engine('sqlite:///tvigle_test.db') #SqlAlchemy connection pool
Base = declarative_base(bind=Db)
Session = sessionmaker(bind=Db)