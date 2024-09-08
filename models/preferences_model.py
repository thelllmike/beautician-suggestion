from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Preferences(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    Customer_ID = Column(Integer, ForeignKey('customers.Customer_ID')) 
    Style_Orientation = Column(String(50))
    Speed_of_Service = Column(String(50))
    Beautician_Interaction_Style = Column(String(50))
    Beautician_Personality_Type = Column(String(50))
    Average_Time = Column(String(50))  # Add the new column here
