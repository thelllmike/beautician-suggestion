from pydantic import BaseModel

class SalonVisualsBase(BaseModel):
    Color: str
    Decor: str
    Lighting: str
    Furniture: str
    WashingStation: str
    StylingStation: str
    WaitingArea: str
    Cluster: str
    CustomerID: int

class SalonVisualsCreate(SalonVisualsBase):
    pass

class SalonVisuals(SalonVisualsBase):
    VisualsPreferenceID: int
    # age: str
    # income_level: str
    # gender: str

class SalonVisual(SalonVisualsBase):
    VisualsPreferenceID: int
    age: str
    income_level: str
    gender: str

    class Config:
        orm_mode = True
