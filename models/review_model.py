from sqlalchemy import Column, Integer, String, DECIMAL, Text, ForeignKey
from database import Base


class Review(Base):
    __tablename__ = "reviews"
    Review_ID = Column(Integer, primary_key=True, index=True)
    Comment = Column(Text)
    Rating = Column(DECIMAL(3, 2))
    Image = Column(String(255))
    Customer_ID = Column(Integer, ForeignKey('customers.Customer_ID'))
    Beautician_ID = Column(Integer, ForeignKey('beauticians.Beautician_ID'))
