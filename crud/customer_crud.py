from sqlalchemy.orm import Session
import models.customer_model as models
import schemas.customer_schema as schemas
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def get_customer_by_email(db: Session, email: str):
    """Fetch a customer from the database by email."""
    return db.query(models.Customer).filter(models.Customer.Email == email).first()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    """Create a new customer in the database."""
    # Check if the email is already registered
    existing_customer = get_customer_by_email(db, customer.Email)
    if existing_customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")
    
    # Proceed with creating the customer if email is not registered
    db_customer = models.Customer(**customer.dict())
    try:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the customer")
    return db_customer

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve a list of customers from the database."""
    return db.query(models.Customer).offset(skip).limit(limit).all()

def get_customer(db: Session, customer_id: int):
    """Retrieve a single customer by ID."""
    return db.query(models.Customer).filter(models.Customer.Customer_ID == customer_id).first()

def update_customer(db: Session, db_customer: models.Customer, customer: schemas.CustomerCreate):
    """Update an existing customer's details."""
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    """Delete a customer from the database by ID."""
    db_customer = db.query(models.Customer).filter(models.Customer.Customer_ID == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return db_customer
