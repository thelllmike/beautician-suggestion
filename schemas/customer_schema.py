from pydantic import BaseModel

class CustomerBase(BaseModel):
    Name: str
    Gender: str
    Age: str  # Change from int to str to accommodate age ranges like "18-34"
    IncomeLevel: str  # New field for income level
    Email: str
    Password: str

class CustomerUpdate(BaseModel):
    Customer_ID: int
    Name: str
    Gender: str
    Age: str
    IncomeLevel: str
    Email: str
    Password: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    Customer_ID: int

    class Config:
        orm_mode = True
