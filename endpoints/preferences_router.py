from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.preferences_model as models
import schemas.preferences_schema as schemas
import crud.preferences_crud as crud
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Preferences)
def create_preferences(preferences: schemas.PreferencesCreate, db: Session = Depends(get_db)):
    return crud.create_preferences(db=db, preferences=preferences)



@router.get("/{customer_id}", response_model=schemas.Preferences)
def read_preferences(customer_id: int, db: Session = Depends(get_db)):
    db_preferences = crud.get_preferences(db, customer_id=customer_id)
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return db_preferences

@router.put("/{customer_id}", response_model=schemas.Preferences)
def update_preferences(customer_id: int, preferences: schemas.PreferencesCreate, db: Session = Depends(get_db)):
    db_preferences = crud.get_preferences(db, customer_id=customer_id)
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return crud.update_preferences(db=db, db_preferences=db_preferences, preferences=preferences)

@router.delete("/{customer_id}", response_model=schemas.Preferences)
def delete_preferences(customer_id: int, db: Session = Depends(get_db)):
    db_preferences = crud.get_preferences(db, customer_id=customer_id)
    if db_preferences is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return crud.delete_preferences(db=db, customer_id=customer_id)
