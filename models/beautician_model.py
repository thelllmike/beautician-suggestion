from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from database import Base

class Beautician(Base):
    __tablename__ = "beauticians"
    Beautician_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100))
    Age = Column(Integer)
    Gender = Column(String(10))
    Position = Column(String(100))
    Rating_Score = Column(DECIMAL(3, 2))
    Characteristics = Column(String(255))
    Image = Column(String(255))
    Salon_ID = Column(Integer, ForeignKey('salons.Salon_ID'))  # Foreign key to Salon

  
