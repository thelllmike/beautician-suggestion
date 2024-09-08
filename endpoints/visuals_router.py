from typing import Tuple
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import crud.visuals_crud as crud
import schemas.visuals_schema as schemas # type: ignore
from database import SessionLocal
import crud.customer_crud as customer_crud
import crud.visuals_crud as visuals_crud
from collections import Counter

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to retrieve common query parameters
def get_customer_attributes(
    gender: str = Query(...),
    age: str = Query(...),
    income_level: str = Query(...),
) -> Tuple[str, str, str]:
    return gender, age, income_level


@router.post("/", response_model=schemas.SalonVisuals)
def create_salon_visuals(salon_visuals: schemas.SalonVisualsCreate, db: Session = Depends(get_db)):
    return crud.create_salon_visuals(db=db, salon_visuals=salon_visuals)

@router.get("/", response_model=list[schemas.SalonVisuals])
def read_salon_visuals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_salon_visuals(db=db, skip=skip, limit=limit)


@router.put("/{visuals_id}", response_model=schemas.SalonVisuals)
def update_salon_visuals(visuals_id: int, salon_visuals: schemas.SalonVisualsCreate, db: Session = Depends(get_db)):
    db_salon_visuals = crud.get_salon_visuals_by_id(db, visuals_id=visuals_id)
    if db_salon_visuals is None:
        raise HTTPException(status_code=404, detail="Salon visuals not found")
    return crud.update_salon_visuals(db=db, db_salon_visuals=db_salon_visuals, salon_visuals=salon_visuals)

@router.delete("/{visuals_id}", response_model=schemas.SalonVisuals)
def delete_salon_visuals(visuals_id: int, db: Session = Depends(get_db)):
    db_salon_visuals = crud.get_salon_visuals_by_id(db, visuals_id=visuals_id)
    if db_salon_visuals is None:
        raise HTTPException(status_code=404, detail="Salon visuals not found")
    return crud.delete_salon_visuals(db=db, visuals_id=visuals_id)


# 1. Specific route for visuals by customer attributes
@router.get("/visuals_by_customer_attributes", response_model=list[schemas.SalonVisuals])
def get_visuals_by_customer_attributes(
    gender: str = Query(...),
    age: str = Query(...),
    income_level: str = Query(...),
    db: Session = Depends(get_db)
):
    # Get customer IDs that match the given criteria
    customer_ids = customer_crud.get_customer_ids_by_attributes(db=db, gender=gender, age=age, income_level=income_level)
    customer_ids = [id_tuple[0] for id_tuple in customer_ids]  # Flatten the list of tuples

    if not customer_ids:
        raise HTTPException(status_code=404, detail="No customers found with the provided criteria.")

    # Get visuals based on the list of customer IDs
    visuals = visuals_crud.get_visuals_by_customer_ids(db=db, customer_ids=customer_ids)
    if not visuals:
        raise HTTPException(status_code=404, detail="No visuals found for the provided customer IDs.")

    return visuals

# 2. General route for reading visuals by ID (less specific)
@router.get("/{visuals_id}", response_model=schemas.SalonVisuals)
def read_salon_visuals_by_id(visuals_id: int, db: Session = Depends(get_db)):
    db_salon_visuals = crud.get_salon_visuals_by_id(db, visuals_id=visuals_id)
    if db_salon_visuals is None:
        raise HTTPException(status_code=404, detail="Salon visuals not found")
    return db_salon_visuals

# @router.get("/visuals_by_customer_attributes", response_model=list[schemas.SalonVisuals])
# def get_visuals_by_customer_attributes(
#     gender: str = Query(...),
#     age: str = Query(...),
#     income_level: str = Query(...),
#     db: Session = Depends(get_db)
# ):
#     # Get customer IDs that match the given criteria
#     customer_ids = customer_crud.get_customer_ids_by_attributes(db=db, gender=gender, age=age, income_level=income_level)
#     customer_ids = [id_tuple[0] for id_tuple in customer_ids]  # Flatten the list of tuples

#     if not customer_ids:
#         raise HTTPException(status_code=404, detail="No customers found with the provided criteria.")

#     # Get visuals based on the list of customer IDs
#     visuals = visuals_crud.get_visuals_by_customer_ids(db=db, customer_ids=customer_ids)
#     if not visuals:
#         raise HTTPException(status_code=404, detail="No visuals found for the provided customer IDs.")

#     return visuals


@router.get("/visuals_by_customer_attributes", response_model=list[schemas.SalonVisuals])
def get_visuals_by_customer_attributes(
    gender: str = Query(...),
    age: str = Query(...),
    income_level: str = Query(...),
    db: Session = Depends(get_db)
):
    # Get customer IDs that match the given criteria
    customer_ids = customer_crud.get_customer_ids_by_attributes(db=db, gender=gender, age=age, income_level=income_level)
    customer_ids = [id_tuple[0] for id_tuple in customer_ids]  # Flatten the list of tuples

    if not customer_ids:
        raise HTTPException(status_code=404, detail="No customers found with the provided criteria.")

    # Get visuals based on the list of customer IDs
    visuals = visuals_crud.get_visuals_by_customer_ids(db=db, customer_ids=customer_ids)
    if not visuals:
        raise HTTPException(status_code=404, detail="No visuals found for the provided customer IDs.")

    # Attach the customer attributes to each visual in the response
    for visual in visuals:
        visual.age = age
        visual.income_level = income_level
        visual.gender = gender

    return visuals



@router.get("/visualscus/{visual_id}", response_model=dict)
def get_customer_attributes_by_visual_id(visual_id: int, db: Session = Depends(get_db)):
    # Retrieve the visual by ID
    visual = visuals_crud.get_salon_visuals_by_id(db, visuals_id=visual_id)
    
    if not visual:
        raise HTTPException(status_code=404, detail="Visual not found")

    # Retrieve the customer associated with the visual
    customer = customer_crud.get_customer(db, customer_id=visual.CustomerID)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Prepare the response with the relevant customer attributes
    response = {
        "gender": customer.Gender,
        "age": customer.Age,
        "income_level": customer.IncomeLevel
    }

    return response


@router.get("/visuals/most_frequent_cluster", response_model=list[schemas.SalonVisual])
def get_visuals_by_most_frequent_cluster(
    customer_attributes: Tuple[str, str, str] = Depends(get_customer_attributes),
    db: Session = Depends(get_db)
):
    gender, age, income_level = customer_attributes

    # Get customer IDs that match the given criteria
    customer_ids = customer_crud.get_customer_ids_by_attributes(db=db, gender=gender, age=age, income_level=income_level)
    customer_ids = [id_tuple[0] for id_tuple in customer_ids]  # Flatten the list of tuples

    if not customer_ids:
        raise HTTPException(status_code=404, detail="No customers found with the provided criteria.")

    # Get all clusters for the matched customer IDs
    clusters = visuals_crud.get_clusters_by_customer_ids(db=db, customer_ids=customer_ids)
    
    if not clusters:
        raise HTTPException(status_code=404, detail="No clusters found for the provided customer IDs.")

    # Count the occurrences of each cluster and find the most frequent one
    cluster_count = Counter([cluster.Cluster for cluster in clusters])  # Extract the actual cluster values
    most_frequent_cluster = cluster_count.most_common(1)[0][0]

    # Get all visuals where the cluster is equal to the most frequent cluster
    visuals = visuals_crud.get_visuals_by_cluster(db=db, cluster=most_frequent_cluster)

    if not visuals:
        raise HTTPException(status_code=404, detail=f"No visuals found for the cluster {most_frequent_cluster}.")

    # Attach the relevant customer attributes to each visual in the response
    relevant_visuals = []
    for visual in visuals:
        # Retrieve the associated customer
        customer = customer_crud.get_customer(db, customer_id=visual.CustomerID)
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer with ID {visual.CustomerID} not found")

        # Convert the ORM object to a dictionary
        visual_dict = visual.__dict__.copy()
        
        # Attach the customer attributes to the visual
        visual_dict['age'] = customer.Age
        visual_dict['income_level'] = customer.IncomeLevel
        visual_dict['gender'] = customer.Gender
        
        relevant_visuals.append(visual_dict)

    return relevant_visuals


