from app import Base
from sqlalchemy import Column, String, Integer
from app import engine


class Person(Base):
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    password = Column(String(45))
    email = Column(String(45))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
