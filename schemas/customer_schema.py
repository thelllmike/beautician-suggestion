from pydantic import BaseModel

class CustomerBase(BaseModel):
    Name: str
    Gender: str
    Age: int
    Email: str
    Password: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    Customer_ID: int
    class Config:
        orm_mode = True
