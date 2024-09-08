import os
import sys
import numpy as np
import pandas as pd
import pickle
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil

# Dynamically add the directory where modelPipeline.py is located to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import modelPipeline now that the path is updated
import modelPipeline as mp

# Create a new router for hair-related routes
router = APIRouter()

# Define the upload folder
UPLOAD_FOLDER = os.path.join(current_dir, "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the hair care recommendations dataset from the pickle file
pickle_file_path = os.path.join(current_dir, 'hair_care_recommendations.pkl')
with open(pickle_file_path, 'rb') as f:
    hair_recommendations = pickle.load(f)

@router.get("/")
def read_root():
    return {"message": "Welcome to the Hair Classification App"}

@router.post("/Process_image/")
async def process_image(file: UploadFile = File(...)):
    # Check if the file is an image
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        raise HTTPException(status_code=400, detail="Invalid image file type")

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call the pipeline to process the image
    try:
        results = mp.Pipeline(file_path)
        hair_dict = {0: 'Curly', 1: 'Short', 2: 'Straight', 3: 'Braided'}  # Match hair type with data in the pickle file
        max_index = np.argmax(results)
        hairType = hair_dict.get(max_index)

        # Check if the hair type was detected correctly
        if hairType is None:
            return JSONResponse(content={"message": "Hair type could not be detected", "filename": file.filename})

        # Filter the recommendations based on hair type
        recommendations = hair_recommendations[hair_recommendations['Hair Type'].str.contains(hairType, case=False, na=False)]

        if recommendations.empty:
            return JSONResponse(content={"message": f"No recommendations available for {hairType}", "filename": file.filename})

        # Convert the filtered recommendations to a list of dictionaries
        recommendations_list = recommendations.to_dict(orient='records')

        return JSONResponse(content={"hairType": hairType, "recommendations": recommendations_list, "filename": file.filename})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")
