from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base


class Salon(Base):
    __tablename__ = "salons"
    Salon_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Location = Column(String(255))
    Rating_score = Column(DECIMAL(3, 2))
    Email = Column(String(100))
    Password = Column(String(100))
    Services = Column(String(255))
