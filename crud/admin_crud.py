from sqlalchemy.orm import Session
import models.admin_model as models
import schemas.admin_schema as schemas

def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admins(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Admin).offset(skip).limit(limit).all()

def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.Admin_ID == admin_id).first()

def update_admin(db: Session, db_admin: models.Admin, admin: schemas.AdminCreate):
    for key, value in admin.dict().items():
        setattr(db_admin, key, value)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.Admin_ID == admin_id).first()
    db.delete(db_admin)
    db.commit()
    return db_admin
