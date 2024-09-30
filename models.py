from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase

#
sqlite_database = "sqlite:///data.db"
engine = create_engine(sqlite_database)

class Base(DeclarativeBase):
    pass


class User_Info(Base):
    __tablename__ = "User_Info"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    text_id = Column(String)
    user_name = Column(Text)
    user_surname = Column(Text)
    username = Column(String)
    text = Column(String)
class Chat_History(Base):
    __tablename__ = "Chat_History"
    id = Column(Integer, primary_key=True, index=True)
    chat = Column(String)
def create_tables():
    Base.metadata.create_all(bind=engine)
