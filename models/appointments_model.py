from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from database import Base


class Appointments(Base):
    __tablename__ = "appointments"
    Appointment_ID = Column(Integer, primary_key=True, index=True)
    Date = Column(Date)
    Time = Column(Time)
    Status = Column(String(50))
    Customer_ID = Column(Integer, ForeignKey('customers.Customer_ID'))
    Beautician_ID = Column(Integer, ForeignKey('beauticians.Beautician_ID'))
    Salon_ID = Column(Integer, ForeignKey('salons.Salon_ID'))


