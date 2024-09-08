from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class SalonVisuals(Base):
    __tablename__ = "salon_visuals"
    VisualsPreferenceID = Column(Integer, primary_key=True, index=True)
    Color = Column(String(255))  # Image URL or file path for color preference
    Decor = Column(String(255))  # Image URL or file path for decor preference
    Lighting = Column(String(255))  # Image URL or file path for lighting preference
    Furniture = Column(String(255))  # Image URL or file path for furniture preference
    WashingStation = Column(String(255))  # Image URL or file path for washing station preference
    StylingStation = Column(String(255))  # Image URL or file path for styling station preference
    WaitingArea = Column(String(255))  # Image URL or file path for waiting area preference
    Cluster = Column(String(255))
    CustomerID = Column(Integer, ForeignKey("customers.Customer_ID"))  # Foreign key to the customer table
  
