from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    child_name = Column(String, index=True)
    characters = Column(String, nullable=True)
    details = Column(String, nullable=True)
    story = Column(Text)