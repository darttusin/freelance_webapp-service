from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

class Users(base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, unique=True)
    user_name = Column(String)
    user_email = Column(String)
    user_password = Column(String,)
    user_description = Column(String) 
    user_img_url = Column(String)


class TgUsers(base):
    __tablename__ = "tgusers"

    user_id = Column(String, ForeignKey("users.user_id"))
    chat_room_id = Column(String)
    tg_name = Column(String)
    tg_id = Column(Integer, unique=True, primary_key=True)

    user = relationship("Users")