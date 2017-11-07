from app import Base
from sqlalchemy import Column, String, Integer
import hashlib
from app import engine


class Person(Base):
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    password = Column(String(45))
    email = Column(String(45))
    about = Column(String(200))

    def avatar(self, size):
        md5 = hashlib.md5()
        md5.update(self.email)
        return 'http://www.gravatar.com/avatar/' + md5.hexdigest() + '?d=mm&s=' + str(size)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
