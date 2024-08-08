from sqlalchemy.orm import Session
import models.salon_model as models
import schemas.salon_schema as schemas

def create_salon(db: Session, salon: schemas.SalonCreate):
    db_salon = models.Salon(**salon.dict())
    db.add(db_salon)
    db.commit()
    db.refresh(db_salon)
    return db_salon

def get_salons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Salon).offset(skip).limit(limit).all()

def get_salon(db: Session, salon_id: int):
    return db.query(models.Salon).filter(models.Salon.Salon_ID == salon_id).first()

def update_salon(db: Session, db_salon: models.Salon, salon: schemas.SalonCreate):
    for key, value in salon.dict().items():
        setattr(db_salon, key, value)
    db.commit()
    db.refresh(db_salon)
    return db_salon

def delete_salon(db: Session, salon_id: int):
    db_salon = db.query(models.Salon).filter(models.Salon.Salon_ID == salon_id).first()
    db.delete(db_salon)
    db.commit()
    return db_salon
