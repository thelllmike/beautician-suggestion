import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.salon_model as models
import schemas.salon_schema as schemas
import crud.salon_crud as crud
from database import SessionLocal
import httpx

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Salon)
def create_salon(salon: schemas.SalonCreate, db: Session = Depends(get_db)):
    return crud.create_salon(db=db, salon=salon)

# @router.get("/", response_model=list[schemas.Salon])
# def read_salons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     salons = crud.get_salons(db, skip=skip, limit=limit)
#     return salons

async def get_coordinates_for_location(location: str, api_key: str):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['geometry']['location']  # returns {'lat': value, 'lng': value}
        return None

@router.get("/", response_model=list[schemas.Salon])
async def read_salons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    salons = crud.get_salons(db, skip=skip, limit=limit)
    
    # Fetch coordinates for each salon asynchronously
    api_key = "AIzaSyBWhC-jpCx47bY-576p7EgJhApi_BMp8Dk"  # Replace with your actual Google API key
    tasks = [get_coordinates_for_location(salon.Location, api_key) for salon in salons]
    coordinates_list = await asyncio.gather(*tasks)
    
    for salon, coordinates in zip(salons, coordinates_list):
        if coordinates:
            salon.latitude = coordinates['lat']
            salon.longitude = coordinates['lng']
    
    return salons

@router.get("/{salon_id}", response_model=schemas.Salon)
def read_salon(salon_id: int, db: Session = Depends(get_db)):
    db_salon = crud.get_salon(db, salon_id=salon_id)
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return db_salon

@router.put("/{salon_id}", response_model=schemas.Salon)
def update_salon(salon_id: int, salon: schemas.SalonCreate, db: Session = Depends(get_db)):
    db_salon = crud.get_salon(db, salon_id=salon_id)
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return crud.update_salon(db=db, db_salon=db_salon, salon=salon)

@router.delete("/{salon_id}", response_model=schemas.Salon)
def delete_salon(salon_id: int, db: Session = Depends(get_db)):
    db_salon = crud.get_salon(db, salon_id=salon_id)
    if db_salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    return crud.delete_salon(db=db, salon_id=salon_id)
