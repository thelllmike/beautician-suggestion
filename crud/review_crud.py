from sqlalchemy import join, select
from sqlalchemy.orm import Session
import models.review_model as models
import schemas.review_schema as schemas
from models.beautician_model import Beautician 



def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review  # Only return the review details, not beautician information

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


#Quary

def get_reviews_with_beautician_info(db: Session, skip: int = 0, limit: int = 10):
    stmt = (
        select(models.Review.Review_ID, 
               Beautician.Beautician_ID, 
               Beautician.Name, 
               models.Review.Comment)
        .select_from(join(models.Review, Beautician, models.Review.Beautician_ID == Beautician.Beautician_ID))
        .offset(skip).limit(limit)
    )
    result = db.execute(stmt).fetchall()

    # Manually convert each row into a dictionary
    reviews = []
    for row in result:
        review_dict = {
            "Review_ID": row[0],
            "Beautician_ID": row[1],
            "Name": row[2],
            "Comment": row[3]
        }
        reviews.append(review_dict)
    
    return reviews


def get_reviews_by_beautician_id(db: Session, beautician_id: int, skip: int = 0, limit: int = 10):
    stmt = (
        select(models.Review.Review_ID, 
               Beautician.Beautician_ID, 
               Beautician.Name, 
               models.Review.Comment,
               Beautician.Image)  # Include the Image field in the select statement
        .select_from(join(models.Review, Beautician, models.Review.Beautician_ID == Beautician.Beautician_ID))
        .where(Beautician.Beautician_ID == beautician_id)
        .offset(skip).limit(limit)
    )
    result = db.execute(stmt).fetchall()

    # Manually convert each row into a dictionary
    reviews = []
    for row in result:
        review_dict = {
            "Review_ID": row[0],
            "Beautician_ID": row[1],
            "Name": row[2],
            "Comment": row[3],
            "Image": row[4]  # Include the Image in the result
        }
        reviews.append(review_dict)
    
    return reviews
