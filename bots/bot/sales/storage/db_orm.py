from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


engine = create_engine("sqlite:///app_db.db", echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(250), nullable=False)
    phone_number = Column(String(250), nullable=False)
    role = Column(String(250), nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    order = Column(String(250), nullable=False)
    order_status = Column(String(250), nullable=False)


class Page(Base):
    __tablename__ = "pages"

    page_id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    image_file_name = Column(String(250), nullable=False)
    inline_buttons_content_file_name = Column(String(250), nullable=False)
    catigory = Column(String(250), nullable=False)

class Display(Base):
    __tablename__ = "display"

    menu_id = Column(Integer, primary_key = True)
    page_id = Column(Integer, nullable= False)


Base.metadata.create_all(engine)