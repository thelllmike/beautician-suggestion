from sqlalchemy.orm import Session
import models.visuals_model as models 
import schemas.visuals_schema as schemas 

def create_salon_visuals(db: Session, salon_visuals: schemas.SalonVisualsCreate):
    db_salon_visuals = models.SalonVisuals(**salon_visuals.dict())
    db.add(db_salon_visuals)
    db.commit()
    db.refresh(db_salon_visuals)
    return db_salon_visuals

def get_salon_visuals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SalonVisuals).offset(skip).limit(limit).all()

def get_salon_visuals_by_id(db: Session, visuals_id: int):
    return db.query(models.SalonVisuals).filter(models.SalonVisuals.VisualsPreferenceID == visuals_id).first()

def update_salon_visuals(db: Session, db_salon_visuals: models.SalonVisuals, salon_visuals: schemas.SalonVisualsCreate):
    for key, value in salon_visuals.dict().items():
        setattr(db_salon_visuals, key, value)
    db.commit()
    db.refresh(db_salon_visuals)
    return db_salon_visuals

def delete_salon_visuals(db: Session, visuals_id: int):
    db_salon_visuals = db.query(models.SalonVisuals).filter(models.SalonVisuals.VisualsPreferenceID == visuals_id).first()
    db.delete(db_salon_visuals)
    db.commit()
    return db_salon_visuals

def get_visuals_by_customer_ids(db: Session, customer_ids: list[int]):
    return db.query(models.SalonVisuals).filter(
        models.SalonVisuals.CustomerID.in_(customer_ids)
    ).all()


# In crud/visuals_crud.py

def get_clusters_by_customer_ids(db: Session, customer_ids: list[int]):
    return db.query(models.SalonVisuals.Cluster).filter(models.SalonVisuals.CustomerID.in_(customer_ids)).all()

# In crud/visuals_crud.py

def get_visuals_by_cluster(db: Session, cluster: str):
    return db.query(models.SalonVisuals).filter(models.SalonVisuals.Cluster == cluster).all()
