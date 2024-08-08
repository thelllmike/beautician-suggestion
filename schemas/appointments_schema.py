from pydantic import BaseModel

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
