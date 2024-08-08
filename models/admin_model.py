from sqlalchemy import Column, Integer, String
from database import Base


class Admin(Base):
    __tablename__ = "admins"
    Admin_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Email = Column(String(100))
    Password = Column(String(100))
