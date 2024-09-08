from pydantic import BaseModel

class BeauticianBase(BaseModel):
    Name: str
    Age: int
    Gender: str
    Position: str
    Rating_Score: float
    Characteristics: str
    Image: str
    Salon_ID: int  # Reference to the Salon

class BeauticianCreate(BeauticianBase):
    pass

class Beautician(BeauticianBase):
    Beautician_ID: int

    class Config:
        orm_mode = True
