from sqlalchemy import Column, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from config import database_url


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_engine(database_url)
SessionLocal = sessionmaker(engine)


def get_sync_session():
    return SessionLocal()
