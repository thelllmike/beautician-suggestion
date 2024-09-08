from sqlalchemy import Column, Integer, String
from database import Base


class Customer(Base):
    __tablename__ = "customers"
    Customer_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Gender = Column(String(10))
    Age = Column(String(50))  # Changed from Integer to String for age range
    IncomeLevel = Column(String(100))  # New column for Income Level
    Email = Column(String(100))
    Password = Column(String(100))
   