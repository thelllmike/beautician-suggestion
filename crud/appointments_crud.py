from sqlalchemy.orm import Session
import models.appointments_model as models
import schemas.appointments_schema as schemas

def create_appointment(db: Session, appointment: schemas.AppointmentsCreate):
    db_appointment = models.Appointments(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Appointments).offset(skip).limit(limit).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointments).filter(models.Appointments.Appointment_ID == appointment_id).first()

def update_appointment(db: Session, db_appointment: models.Appointments, appointment: schemas.AppointmentsCreate):
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointments).filter(models.Appointments.Appointment_ID == appointment_id).first()
    db.delete(db_appointment)
    db.commit()
    return db_appointment
