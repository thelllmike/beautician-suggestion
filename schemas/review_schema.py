from pydantic import BaseModel

class ReviewBase(BaseModel):
    Comment: str
    Rating: float
    Image: str

class ReviewCreate(ReviewBase):
    Customer_ID: int
    Beautician_ID: int

class ReviewWithBeauticianInfo(BaseModel):
    Review_ID: int
    Beautician_ID: int
    Name: str
    Comment: str
    Image: str

class Review(ReviewBase):
    Review_ID: int
    class Config:
        orm_mode = True
