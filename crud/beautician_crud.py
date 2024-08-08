from sqlalchemy.orm import Session
import models.beautician_model as models
import schemas.beautician_schema as schemas

def create_beautician(db: Session, beautician: schemas.BeauticianCreate):
    db_beautician = models.Beautician(**beautician.dict())
    db.add(db_beautician)
    db.commit()
    db.refresh(db_beautician)
    return db_beautician

def get_beauticians(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Beautician).offset(skip).limit(limit).all()

def get_beautician(db: Session, beautician_id: int):
    return db.query(models.Beautician).filter(models.Beautician.Beautician_ID == beautician_id).first()

def update_beautician(db: Session, db_beautician: models.Beautician, beautician: schemas.BeauticianCreate):
    for key, value in beautician.dict().items():
        setattr(db_beautician, key, value)
    db.commit()
    db.refresh(db_beautician)
    return db_beautician

def delete_beautician(db: Session, beautician_id: int):
    db_beautician = db.query(models.Beautician).filter(models.Beautician.Beautician_ID == beautician_id).first()
    db.delete(db_beautician)
    db.commit()
    return db_beautician
