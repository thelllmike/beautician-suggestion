from sqlalchemy.orm import Session
import models.review_model as models
import schemas.review_schema as schemas

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.Review_ID == review_id).first()

def update_review(db: Session, db_review: models.Review, review: schemas.ReviewCreate):
    for key, value in review.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.Review_ID == review_id).first()
    db.delete(db_review)
    db.commit()
    return db_review
