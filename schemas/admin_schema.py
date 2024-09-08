from pydantic import BaseModel

class AdminBase(BaseModel):
    Name: str
    Email: str
    Password: str

class AdminCreate(AdminBase):
    pass

class Admin(AdminBase):
    Admin_ID: int
    class Config:
        orm_mode = True
