from pydantic import BaseModel

class SalonBase(BaseModel):
    Name: str
    Location: str
    Rating_score: float
    Email: str
    Password: str
    Services: str

class SalonCreate(SalonBase):
    pass

class Salon(SalonBase):
    Salon_ID: int
    class Config:
        orm_mode = True
