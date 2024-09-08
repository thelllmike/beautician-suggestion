from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models.customer_model as models
import schemas.customer_schema as schemas
import crud.customer_crud as crud
from database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db=db, customer=customer)

@router.get("/", response_model=list[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer



@router.put("/update_customer", response_model=schemas.Customer)
def update_customer(customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer.Customer_ID)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db=db, db_customer=db_customer, customer=customer)


@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.delete_customer(db=db, customer_id=customer_id)

@router.get("/customer_ids/", response_model=list[int])
def get_customer_ids(gender: str, age: str, income_level: str, db: Session = Depends(get_db)):
    customer_ids = crud.get_customer_ids_by_attributes(db, gender=gender, age=age, income_level=income_level)
    if not customer_ids:
        raise HTTPException(status_code=404, detail="No customers found with the given attributes")
    return [id[0] for id in customer_ids]
