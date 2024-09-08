from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.appointments_model as models
import schemas.appointments_schema as schemas
import crud.appointments_crud as crud
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Appointments)
def create_appointment(appointment: schemas.AppointmentsCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db=db, appointment=appointment)

@router.get("/", response_model=list[schemas.Appointments])
def read_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments

@router.get("/{appointment_id}", response_model=schemas.Appointments)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.put("/{appointment_id}", response_model=schemas.Appointments)
def update_appointment(appointment_id: int, appointment: schemas.AppointmentsCreate, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.update_appointment(db=db, db_appointment=db_appointment, appointment=appointment)

@router.delete("/{appointment_id}", response_model=schemas.Appointments)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.delete_appointment(db=db, appointment_id=appointment_id)


@router.get("/customer/{customer_id}", response_model=list[schemas.Appointments])
def read_appointments_by_customer(customer_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_customer(db, customer_id=customer_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this customer")
    return appointments