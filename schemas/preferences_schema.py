from pydantic import BaseModel

class PreferencesBase(BaseModel):
    Style_Orientation: str
    Speed_of_Service: str
    Beautician_Interaction_Style: str
    Beautician_Personality_Type: str
    Average_Time: str  # Add this line

class PreferencesCreate(PreferencesBase):
    Customer_ID: int  # Add this line

class Preferences(PreferencesBase):
    Customer_ID: int

    class Config:
        orm_mode = True
