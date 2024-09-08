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