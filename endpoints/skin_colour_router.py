from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
import numpy as np
import cv2
import pandas as pd
import os

app = FastAPI()
router = APIRouter()

# Define the correct path to the dataset file inside the 'endpoints' directory
makeup_dataset_path = os.path.join(os.path.dirname(__file__), 'skintone-makeup_dataset.pkl')

# Print the absolute path for debugging
print(f"Absolute path to dataset: {makeup_dataset_path}")

# Check if the dataset file exists
if not os.path.exists(makeup_dataset_path):
    raise FileNotFoundError(f"The dataset file was not found at {makeup_dataset_path}")

# Load the skin tone to makeup color dataset
makeup_df = pd.read_pickle(makeup_dataset_path)

def map_skin_tone(dominant_color):
    skin_tones = {
        "Very Fair": {
            "rgb_min": np.array([255, 230, 200]),
            "rgb_max": np.array([255, 245, 230]),
        },
        "Fair": {
            "rgb_min": np.array([255, 219, 172]),
            "rgb_max": np.array([255, 240, 219]),
        },
        "Light": {
            "rgb_min": np.array([241, 194, 125]),
            "rgb_max": np.array([255, 224, 189]),
        },
        "Light Medium": {
            "rgb_min": np.array([220, 175, 110]),
            "rgb_max": np.array([245, 200, 160]),
        },
        "Medium": {
            "rgb_min": np.array([198, 134, 66]),
            "rgb_max": np.array([233, 177, 139]),
        },
        "Tan": {
            "rgb_min": np.array([180, 120, 80]),
            "rgb_max": np.array([210, 160, 120]),
        },
        "Olive": {
            "rgb_min": np.array([150, 90, 50]),
            "rgb_max": np.array([190, 130, 100]),
        },
        "Brown": {
            "rgb_min": np.array([121, 85, 72]),
            "rgb_max": np.array([169, 104, 80]),
        },
        "Dark Brown": {
            "rgb_min": np.array([105, 70, 55]),
            "rgb_max": np.array([130, 85, 70]),
        },
        "Dark": {
            "rgb_min": np.array([91, 60, 17]),
            "rgb_max": np.array([133, 94, 66]),
        },
        "Very Dark": {
            "rgb_min": np.array([70, 40, 20]),
            "rgb_max": np.array([100, 60, 35]),
        },
        "Deep": {
            "rgb_min": np.array([64, 40, 19]),
            "rgb_max": np.array([102, 69, 38]),
        },
        "Deepest": {
            "rgb_min": np.array([50, 30, 15]),
            "rgb_max": np.array([80, 45, 25]),
        }
    }

    closest_tone_name = None
    closest_distance = float('inf')

    for tone_name, tone_data in skin_tones.items():
        rgb_min = tone_data["rgb_min"]
        rgb_max = tone_data["rgb_max"]

        # Calculate the distance between the dominant color and the skin tone range
        clipped_color = np.clip(dominant_color, rgb_min, rgb_max)
        distance = np.linalg.norm(clipped_color - dominant_color)

        if distance < closest_distance:
            closest_distance = distance
            closest_tone_name = tone_name

    return closest_tone_name

@router.post("/upload/")
async def analyze_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image from BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, _ = image_rgb.shape

    # Define regions for the cheeks
    left_cheek = image_rgb[int(height*0.4):int(height*0.6), int(width*0.25):int(width*0.4)]
    right_cheek = image_rgb[int(height*0.4):int(height*0.6), int(width*0.6):int(width*0.75)]

    # Calculate the dominant color across the cheek regions using median
    left_cheek_color = np.median(left_cheek, axis=(0, 1))
    right_cheek_color = np.median(right_cheek, axis=(0, 1))

    # Average the colors of both cheeks
    dominant_color = np.median([left_cheek_color, right_cheek_color], axis=0)

    # Map the dominant color to the closest skin tone
    skin_tone_name = map_skin_tone(dominant_color)

    # Find all matching makeup colors based on the detected skin tone
    makeup_suggestions = makeup_df.loc[makeup_df['Skin Tone'] == skin_tone_name].copy()

    # Convert the dataframe to a list of dictionaries
    makeup_suggestions = makeup_suggestions.to_dict(orient='records')
    
    if not makeup_suggestions:
        raise HTTPException(status_code=404, detail="No makeup suggestions found for this skin tone.")

    return {
        "skin_tone": skin_tone_name,
        "makeup_suggestions": makeup_suggestions  # Return all matching suggestions
    }
