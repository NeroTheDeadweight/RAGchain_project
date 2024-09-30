from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Chat_History
sqlite_database = "sqlite:///data.db"
engine = create_engine(sqlite_database, echo=True)

def save_todb(mess: str):
    with Session(autoflush=False, bind=engine) as db:
        text = Chat_History(chat=mess)

        db.add(text)
        db.commit()  # сохраняем изменения
        db.refresh(text)  # обновляем состояние объекта
        print(text.chat)  # можно получить установленный id


def get_chat_history():
    with Session(autoflush=False, bind=engine) as db:
        history = db.query(Chat_History).all()
        s = []
        for p in history:
            s.append(p.chat)
        return s