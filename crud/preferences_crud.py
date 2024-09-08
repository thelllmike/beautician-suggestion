from sqlalchemy.orm import Session
import models.preferences_model as models
import schemas.preferences_schema as schemas



def create_preferences(db: Session, preferences: schemas.PreferencesCreate):
    db_preferences = models.Preferences(**preferences.dict())
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def get_preferences(db: Session, customer_id: int):
    return db.query(models.Preferences).filter(models.Preferences.Customer_ID == customer_id).first()

def update_preferences(db: Session, db_preferences: models.Preferences, preferences: schemas.PreferencesCreate):
    for key, value in preferences.dict().items():
        setattr(db_preferences, key, value)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def delete_preferences(db: Session, customer_id: int):
    db_preferences = db.query(models.Preferences).filter(models.Preferences.Customer_ID == customer_id).first()
    db.delete(db_preferences)
    db.commit()
    return db_preferences
