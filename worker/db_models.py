from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    result = Column(Integer, nullable=False, default=0)
