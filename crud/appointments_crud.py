from sqlalchemy.orm import Session
import models.appointments_model as models
import schemas.appointments_schema as schemas

def create_appointment(db: Session, appointment: schemas.AppointmentsCreate):
    db_appointment = models.Appointments(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return schemas.Appointments.from_orm(db_appointment)

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    appointments = db.query(models.Appointments).offset(skip).limit(limit).all()
    return [schemas.Appointments.from_orm(app) for app in appointments]

def get_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointments).filter(models.Appointments.Appointment_ID == appointment_id).first()
    if db_appointment:
        return schemas.Appointments.from_orm(db_appointment)
    return None

def update_appointment(db: Session, db_appointment: models.Appointments, appointment: schemas.AppointmentsCreate):
    for key, value in appointment.dict().items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return schemas.Appointments.from_orm(db_appointment)

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointments).filter(models.Appointments.Appointment_ID == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return schemas.Appointments.from_orm(db_appointment)
    return None


def get_appointments_by_customer(db: Session, customer_id: int):
    appointments = db.query(models.Appointments).filter(models.Appointments.Customer_ID == customer_id).all()
    return [schemas.Appointments.from_orm(app) for app in appointments]