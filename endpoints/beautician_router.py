from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.beautician_model as models
import schemas.beautician_schema as schemas
import crud.beautician_crud as crud
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Beautician)
def create_beautician(beautician: schemas.BeauticianCreate, db: Session = Depends(get_db)):
    return crud.create_beautician(db=db, beautician=beautician)

@router.get("/", response_model=list[schemas.Beautician])
def read_beauticians(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    beauticians = crud.get_beauticians(db, skip=skip, limit=limit)
    return beauticians

@router.get("/{beautician_id}", response_model=schemas.Beautician)
def read_beautician(beautician_id: int, db: Session = Depends(get_db)):
    db_beautician = crud.get_beautician(db, beautician_id=beautician_id)
    if db_beautician is None:
        raise HTTPException(status_code=404, detail="Beautician not found")
    return db_beautician

@router.put("/{beautician_id}", response_model=schemas.Beautician)
def update_beautician(beautician_id: int, beautician: schemas.BeauticianCreate, db: Session = Depends(get_db)):
    db_beautician = crud.get_beautician(db, beautician_id=beautician_id)
    if db_beautician is None:
        raise HTTPException(status_code=404, detail="Beautician not found")
    return crud.update_beautician(db=db, db_beautician=db_beautician, beautician=beautician)

@router.delete("/{beautician_id}", response_model=schemas.Beautician)
def delete_beautician(beautician_id: int, db: Session = Depends(get_db)):
    db_beautician = crud.get_beautician(db, beautician_id=beautician_id)
    if db_beautician is None:
        raise HTTPException(status_code=404, detail="Beautician not found")
    return crud.delete_beautician(db=db, beautician_id=beautician_id)
