from sqlalchemy import Column, Integer, String, Float, Boolean 
from database import Base, SessionLocal, engine

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)


class WorkerDB(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key= True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    role = Column(String, nullable=False)