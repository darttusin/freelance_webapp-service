from sqlalchemy import (
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    Boolean, 
    Float
)
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
    

class Portfolios(base):
    __tablename__ = 'portfolios'   

    user_id = Column(String, ForeignKey("users.user_id"))
    portfolio_id = Column(String, primary_key=True, unique=True)
    portfolio_title = Column(String)
    portfolio_description = Column(String)
    portfolio_img_url = Column(String)
    for_delete = Column(Boolean)  

    user = relationship("Users")

class Parameters(base):
    __tablename__ = 'parameters'

    parameter_id = Column(String, primary_key=True, unique=True)
    description = Column(String)

class Statuses(base):
    __tablename__ = 'statuses'

    status_id = Column(String, primary_key=True, unique=True)
    description = Column(String, nullable=False)

class Adverts(base):
    __tablename__ = 'adverts'

    user_id = Column(String, ForeignKey("users.user_id"))
    advert_id = Column(String, primary_key=True, unique=True)
    advert_text = Column(String)
    advert_title = Column(String)
    advert_city = Column(String)
    advert_status = Column(String)
    advert_price = Column(Integer)
    for_delete = Column(Boolean)

    user = relationship("Users")


class Reviews(base):
    __tablename__ = 'reviews'

    review_id = Column(String, primary_key=True, unique=True)
    advert_id = Column(String)
    user_id = Column(String, ForeignKey("users.user_id"))
    review_author_id = Column(String)
    review_author_comment = Column(String)
    estimation = Column(Integer)

    user = relationship("Users")


class Filters(base):
    __tablename__ = 'filters'

    filter_id = Column(String, primary_key=True, unique=True)
    advert_id = Column(String, ForeignKey("adverts.advert_id"))
    parameter_id = Column(String, ForeignKey("parameters.parameter_id"))
    value = Column(String)
    for_delete = Column(Boolean)

    advert = relationship("Adverts")
    parameter = relationship("Parameters")

class Responses(base):
    __tablename__ = 'responses'

    response_id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    advert_id = Column(String, ForeignKey("adverts.advert_id"))
    response_text = Column(String)
    response_status = Column(String)
    response_price = Column(Integer)
    for_delete = Column(Boolean)

    user = relationship("Users")
    advert = relationship("Adverts")


class ChatRooms(base):
    __tablename__ = 'chatrooms'

    chat_room_id = Column(Integer, primary_key=True, unique=True)
    advert_id = Column(String, ForeignKey("adverts.advert_id"))
    customer_id = Column(String)
    performer_id = Column(String)
    last_message = Column(String)
    chat_opened = Column(Boolean)

    advert = relationship("Adverts")


class Messages(base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, unique=True)
    chat_room_id = Column(Integer, ForeignKey("chatrooms.chat_room_id"))
    message_sender = Column(String)
    message_text = Column(String)
    message_time = Column(String)


    chatroom = relationship("ChatRooms")


class Admins(base):
    __tablename__ = 'admins'

    admin_id = Column(String, primary_key=True, unique=True)
    admin_email = Column(String)
    admin_login = Column(String)
    admin_password = Column(String)
    admin_role = Column(String)


class UserStats(base):
    __tablename__ = "userstats"

    stat_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    count_views = Column(Integer)
    rating = Column(Float)
    count_reviews = Column(Integer)
    count_jobs = Column(Integer)

    user = relationship("Users")

class TgUsers(base):
    __tablename__ = "tgusers"

    user_id = Column(String, ForeignKey("users.user_id"))
    chat_room_id = Column(String)
    tg_name = Column(String)
    tg_id = Column(Integer, unique=True, primary_key=True)

    user = relationship("Users")


class Offers(base):
    __tablename__ = "offers"

    offer_id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    advert_id = Column(String, ForeignKey("adverts.advert_id"))
    offer_status = Column(String)
    for_delete = Column(Boolean)

    user = relationship("Users")
    advert = relationship("Adverts")
