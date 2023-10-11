from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_engine(settings.database_url, echo=True)
Session = sessionmaker(engine)
session = Session()

