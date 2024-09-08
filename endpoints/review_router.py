from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models.review_model as models
import schemas.review_schema as schemas
import crud.review_crud as crud
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)



@router.get("/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.put("/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return crud.update_review(db=db, db_review=db_review, review=review)

@router.delete("/{review_id}", response_model=schemas.Review)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return crud.delete_review(db=db, review_id=review_id)

#quary


@router.get("/", response_model=List[schemas.ReviewWithBeauticianInfo])
def read_reviews_with_beautician_info(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_with_beautician_info(db, skip=skip, limit=limit)
    return [schemas.ReviewWithBeauticianInfo(**review) for review in reviews]

@router.get("/beautician/{beautician_id}", response_model=List[schemas.ReviewWithBeauticianInfo])
def read_reviews_by_beautician_id(
    beautician_id: int, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    reviews = crud.get_reviews_by_beautician_id(db, beautician_id=beautician_id, skip=skip, limit=limit)
    return [schemas.ReviewWithBeauticianInfo(**review) for review in reviews]
