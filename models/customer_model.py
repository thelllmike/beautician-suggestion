from sqlalchemy import Column, Integer, String
from database import Base


class Customer(Base):
    __tablename__ = "customers"
    Customer_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Gender = Column(String(10))
    Age = Column(Integer)
    Email = Column(String(100))
    Password = Column(String(100))
