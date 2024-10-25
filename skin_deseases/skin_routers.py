import os
from typing import Optional
import cv2
import numpy as np
import joblib
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import load_model

router = APIRouter()

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the model files
cnn_model_path = os.path.join(current_dir, 'cnn_classifier_model.h5')
xgb_model_path = os.path.join(current_dir, 'xgb_classifier_model.pkl')
svm_model_path = os.path.join(current_dir, 'svm_classifier_model.pkl')

# Load the saved models
cnn_model = load_model(cnn_model_path)
xgb_model = joblib.load(xgb_model_path)
svm_model = joblib.load(svm_model_path)

# Load the treatment recommendations .pkl file
pkl_file_path = os.path.join(current_dir, 'treatment_recommendations.pkl')
treatment_df = joblib.load(pkl_file_path)

# Temporary directory for saving uploaded images
TEMP_DIR = os.path.join(current_dir, "temp_images/")
os.makedirs(TEMP_DIR, exist_ok=True)

# Pydantic model for the response
class AcneDetectionResponse(BaseModel):
    affected_percentage: float
    message: str
    treatment: Optional[dict] = None  # Optional treatment suggestion

# Function to preprocess a single image
def preprocess_image(image_path, img_size=(128, 128)):
    image = cv2.imread(image_path)
    image = cv2.resize(image, img_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image / 255.0  # Normalize the image
    return np.expand_dims(image, axis=0)  # Add batch dimension

# Function to extract features using the CNN model
def extract_features(model, image):
    features = model.predict(image)
    features = features.reshape(1, -1)  # Flatten to 1D for a single image
    return features

# Updated function to suggest treatment based on the predicted class and affected percentage
def suggest_treatment(predicted_class, affected_percentage):
    # Ensure the first letter is capitalized for uniform matching
    predicted_class = predicted_class.capitalize()
    
    # Filter the treatment dataframe based on the issue and affected percentage
    filtered_df = treatment_df[
        (treatment_df['Issue'] == predicted_class) &
        (treatment_df['Affected_Percentage'] <= affected_percentage)
    ]
    
    if not filtered_df.empty:
        suggestion = filtered_df.iloc[0].to_dict()
        return suggestion
    else:
        return {"message": "No treatment found for this issue and percentage"}

# Function to calculate the percentage of affected area in a given image and return treatment suggestion
def calculate_affected_percentage(cnn_model, xgb_model, svm_model, image_path):
    # Preprocess the image
    image = preprocess_image(image_path)
    
    # Extract features using the CNN model
    features = extract_features(cnn_model, image)
    
    # Predict using the XGBoost model
    xgb_prediction = int(xgb_model.predict(features)[0])
    
    # Predict using the SVM model
    svm_prediction = int(svm_model.predict(features)[0])
    
    # Label mapping
    label_mapping = {0: 'normal', 1: 'acne', 2: 'pimples', 3: 'dark spots'}
    xgb_predicted_label = label_mapping[xgb_prediction]
    svm_predicted_label = label_mapping[svm_prediction]
    
    if xgb_predicted_label != 'normal':
        # Load the original image for bounding box visualization
        original_image = cv2.imread(image_path)
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Convert to grayscale and find contours
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate affected area
        total_image_area = original_image.shape[0] * original_image.shape[1]
        affected_area = sum(cv2.contourArea(c) for c in contours)
        affected_percentage = (affected_area / total_image_area) * 100
        
        # Suggest treatment based on the prediction and affected percentage
        suggested_treatment = suggest_treatment(xgb_predicted_label, affected_percentage)
        
        return affected_percentage, xgb_predicted_label, svm_predicted_label, suggested_treatment
    else:
        # For normal skin, use the affected percentage to suggest a treatment
        affected_percentage = 0  # Assuming 0% for normal skin
        suggested_treatment = suggest_treatment('Normal', affected_percentage)
        return affected_percentage, 'normal', 'normal', suggested_treatment

@router.post("/detect_acne", response_model=AcneDetectionResponse)
async def detect_acne(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to the temporary directory
        file_path = os.path.join(TEMP_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Calculate the affected percentage and get treatment suggestion
        affected_percentage, xgb_label, svm_label, suggested_treatment = calculate_affected_percentage(cnn_model, xgb_model, svm_model, file_path)
        
        # Remove the temporary file after processing
        os.remove(file_path)

        message = f"{xgb_label.capitalize()} detected, " if affected_percentage > 0 else "Normal skin detected"
        
        # Add treatment suggestion to the response
        response = AcneDetectionResponse(affected_percentage=affected_percentage, message=message, treatment=suggested_treatment)
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
