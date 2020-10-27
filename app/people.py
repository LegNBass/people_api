"""
This file contains the definition of the Person object
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class People(Base):
    """
    ORM definition of the people table
    """
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(2355))
    email = Column(String(255))
    age = Column(Integer)
    version = Column(Integer)

    def as_dict(self):
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }
