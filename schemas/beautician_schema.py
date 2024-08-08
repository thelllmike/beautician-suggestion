from pydantic import BaseModel

class BeauticianBase(BaseModel):
    Name: str
    Age: int
    Gender: str
    Position: str
    Rating_Score: float
    Characteristics: str
    Image: str

class BeauticianCreate(BeauticianBase):
    pass

class Beautician(BeauticianBase):
    Beautician_ID: int
    class Config:
        orm_mode = True
