from pydantic import BaseModel
from datetime import date, time

class AppointmentsBase(BaseModel):
    Date: str
    Time: str
    Status: str

class AppointmentsCreate(AppointmentsBase):
    Customer_ID: int
    Beautician_ID: int
    Salon_ID: int

class Appointments(AppointmentsBase):
    Appointment_ID: int

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            Date=obj.Date.strftime('%Y-%m-%d'),  # Convert date to string
            Time=obj.Time.strftime('%H:%M:%S'),  # Convert time to string
            Status=obj.Status,
            Appointment_ID=obj.Appointment_ID,
            Customer_ID=obj.Customer_ID,
            Beautician_ID=obj.Beautician_ID,
            Salon_ID=obj.Salon_ID
        )
