import os
import pickle
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, APIRouter
from typing import List
from tensorflow.keras.models import model_from_json
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.layers import Layer

router = APIRouter()

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to the model files
pkl_path = os.path.join(current_dir, 'newmodel_with_attention.pkl')
json_path = os.path.join(current_dir, 'newmodel_with_attention.json')
weights_path = os.path.join(current_dir, 'newmodel_with_attention_weights.weights.h5')

# Define the custom SelfAttention layer
@tf.keras.utils.register_keras_serializable()
class SelfAttention(Layer):
    def __init__(self, **kwargs):
        super(SelfAttention, self).__init__(**kwargs)

    def build(self, input_shape):
        super(SelfAttention, self).build(input_shape)

    def call(self, inputs):
        attention_weights = tf.keras.layers.Softmax(axis=-1)(inputs)
        attention_output = inputs * attention_weights
        return attention_output

    def compute_output_shape(self, input_shape):
        return input_shape

# Load the `.pkl` file
with open(pkl_path, 'rb') as pkl_file:
    model_data = pickle.load(pkl_file)

# Verify paths are correct and point to existing files
if not os.path.exists(json_path):
    raise FileNotFoundError(f"The JSON model file was not found at the path: {json_path}")
if not os.path.exists(weights_path):
    raise FileNotFoundError(f"The weights file was not found at the path: {weights_path}")

# Load the model architecture and weights with the custom layer included
with open(json_path, 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json, custom_objects={"SelfAttention": SelfAttention})
model.load_weights(weights_path)

# Function to preprocess image
def preprocess_image(image_bytes, target_size=(64, 64)):
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0  # Normalize the image
    return img_array

# Define input data model using Form and File
@router.post("/predict/")
async def predict(
    Color: List[UploadFile] = File(...),
    Decor: List[UploadFile] = File(...),
    Lightning: List[UploadFile] = File(...),
    Furniture: List[UploadFile] = File(...),
    StylingStation: List[UploadFile] = File(...),
    WashingStation: List[UploadFile] = File(...),
    WaitingArea: List[UploadFile] = File(...),
    Age: float = Form(...),
    Gender: int = Form(...),
    IncomeLevel: int = Form(...)
):
    try:
        # Preprocess all images
        X_color = np.array([preprocess_image(await file.read()) for file in Color])
        X_decor = np.array([preprocess_image(await file.read()) for file in Decor])
        X_lightning = np.array([preprocess_image(await file.read()) for file in Lightning])
        X_furniture = np.array([preprocess_image(await file.read()) for file in Furniture])
        X_styling = np.array([preprocess_image(await file.read()) for file in StylingStation])
        X_washing = np.array([preprocess_image(await file.read()) for file in WashingStation])
        X_waiting = np.array([preprocess_image(await file.read()) for file in WaitingArea])

        # Ensure image arrays are correctly shaped
        X_color = X_color.reshape(len(X_color), 64, 64, 3)
        X_decor = X_decor.reshape(len(X_decor), 64, 64, 3)
        X_lightning = X_lightning.reshape(len(X_lightning), 64, 64, 3)
        X_furniture = X_furniture.reshape(len(X_furniture), 64, 64, 3)
        X_styling = X_styling.reshape(len(X_styling), 64, 64, 3)
        X_washing = X_washing.reshape(len(X_washing), 64, 64, 3)
        X_waiting = X_waiting.reshape(len(X_waiting), 64, 64, 3)

        # Prepare demographic inputs
        age = np.array([Age]).reshape(1, 1)
        gender = np.array([Gender]).reshape(1, 1)
        income = np.array([IncomeLevel]).reshape(1, 1)

        # Predict using the model
        inputs = [X_color, X_decor, X_lightning, X_furniture, X_styling, X_washing, X_waiting, age, gender, income]
        prediction = model.predict(inputs)
        predicted_cluster = np.argmax(prediction, axis=1)[0]

        return {"predicted_cluster": int(predicted_cluster)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
