import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd

import crud.review_crud as crud  # Correct import path
from models import admin_model, beautician_model, customer_model, preferences_model, appointments_model, review_model, visuals_model
from endpoints import admin_router, beautician_router, salon_router, customer_router, preferences_router, appointments_router, review_router, skin_router, visuals_router, skin_colour_router ,review
from cluster import cluster_router
from skin_deseases import skin_routers
from hair import hair_router
from database import Base, SessionLocal, engine
import models.beautician_model as models
import models.salon_model as salon_models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(admin_router.router, prefix="/admins", tags=["admins"])
app.include_router(beautician_router.router, prefix="/beauticians", tags=["beauticians"])
app.include_router(salon_router.router, prefix="/salons", tags=["salons"])
app.include_router(customer_router.router, prefix="/customers", tags=["customers"])
app.include_router(preferences_router.router, prefix="/preferences", tags=["preferences"])
app.include_router(appointments_router.router, prefix="/appointments", tags=["appointments"])
app.include_router(review_router.router, prefix="/reviews", tags=["reviews"])
app.include_router(visuals_router.router, prefix="/visuals", tags=["visuals"])
app.include_router(cluster_router.router, prefix="/cluster", tags=["cluster"])  # Add the cluster router
app.include_router(skin_router.router, prefix="/skin", tags=["skin"])
app.include_router(skin_routers.router, prefix="/skin_deseases", tags=["skin_deseases"])
app.include_router(skin_colour_router.router, prefix="/skin_color", tags=["skin_color"])
app.include_router(review.router, prefix="/review", tags=["review"])
app.include_router(hair_router.router, prefix="/hair", tags=["hair"])


class Preference(BaseModel):
    styleOrientation: List[str]
    speedOfService: List[str]
    beauticianInteractionStyle: List[str]
    beauticianPersonalityType: List[str]
    averageTime: List[str]

# Load the model and tokenizer
MODEL_PATH = 'path_to_save_model'
TOKENIZER_PATH = 'path_to_save_tokenizer'
tokenizer = BertTokenizer.from_pretrained(TOKENIZER_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load the emoji sentiment analysis model
emoji_model = load_model('emoji_sentiment_model.h5')

# Load the encoders
emoji_encoder = LabelEncoder()
emoji_encoder.classes_ = np.load('emoji_classes.npy', allow_pickle=True)  # Load emoji classes

sentiment_encoder = LabelEncoder()
sentiment_encoder.classes_ = np.load('sentiment_classes.npy', allow_pickle=True)  # Load sentiment classes

# Function to extract emojis from text
def extract_emojis(text):
    return [char for char in text if char in emoji_encoder.classes_]

def predict_emoji_sentiment(emojis):
    emoji_indices = emoji_encoder.transform(emojis)
    emoji_indices = np.array(emoji_indices).reshape(-1, 1)
    predictions = emoji_model.predict(emoji_indices)
    predicted_sentiments = np.argmax(predictions, axis=1)
    predicted_sentiments = [sentiment_encoder.inverse_transform([pred])[0] for pred in predicted_sentiments]
    return predicted_sentiments

def predict_sentiment(review):
    encoded_review = tokenizer.encode_plus(
        review,
        max_length=128,
        truncation=True,
        padding='max_length',
        return_tensors="pt"
    )
    input_ids = encoded_review['input_ids'].to(device)
    attention_mask = encoded_review['attention_mask'].to(device)
    with torch.no_grad():
        output = model(input_ids, attention_mask=attention_mask)
        logits = output.logits
    sentiment_score = torch.softmax(logits, dim=1)[:, 1].item()
    return sentiment_score

@app.post("/recommend/")
async def recommend_beauticians(preferences: Preference, db: Session = Depends(get_db)):
    # Fetch reviews with beautician details
    reviews_data = crud.get_reviews_with_beautician_info(db)
    beauticians = pd.DataFrame(reviews_data)
    beauticians['sentiment_score'] = beauticians['Comment'].apply(predict_sentiment)

    def score_beautician(row):
        score = row['sentiment_score'] * 10
        review_text = row['Comment'].lower()
        for pref, keywords in preferences.dict().items():
            if any(keyword.lower() in review_text for keyword in keywords):
                score += 1
        
        # Adjust score based on emoji sentiment analysis
        emojis = extract_emojis(row['Comment'])
        if emojis:
            emoji_sentiments = predict_emoji_sentiment(emojis)
            for sentiment in emoji_sentiments:
                if sentiment == 'positive':
                    score += 0.50
                elif sentiment == 'negative':
                    score -= 0.50

        return score

    beauticians['score'] = beauticians.apply(score_beautician, axis=1)

    # Remove duplicate beauticians by keeping the highest scored entry for each
    recommended = beauticians.sort_values(by='score', ascending=False).drop_duplicates(subset=['Beautician_ID'], keep='first')

    # Get unique beautician IDs from the sorted recommendations
    beautician_ids = recommended['Beautician_ID'].tolist()

    # Fetch the beautician details along with their associated salon names and IDs
    beauticians_details = (
        db.query(models.Beautician, salon_models.Salon.Name.label("Salon_Name"), salon_models.Salon.Salon_ID)
        .join(salon_models.Salon, models.Beautician.Salon_ID == salon_models.Salon.Salon_ID)
        .filter(models.Beautician.Beautician_ID.in_(beautician_ids))
        .all()
    )

    # Create a dictionary for quick lookup
    beautician_dict = {b.Beautician.Beautician_ID: (b.Beautician, b.Salon_Name, b.Salon_ID) for b in beauticians_details}

    # Combine the beautician details with the scores and keep the order
    recommendations = []
    for index, row in recommended.iterrows():
        beautician_data = beautician_dict.get(row['Beautician_ID'])
        if beautician_data:
            beautician, salon_name, salon_id = beautician_data
            beautician_info = {
                "Beautician_ID": beautician.Beautician_ID,
                "Name": beautician.Name,
                "Age": beautician.Age,
                "Gender": beautician.Gender,
                "Position": beautician.Position,
                "Rating_Score": beautician.Rating_Score,
                "Characteristics": beautician.Characteristics,
                "Image": beautician.Image,
                "Salon_Name": salon_name,
                "Salon_ID": salon_id,  
                "score": row['score']
            }
            recommendations.append(beautician_info)

    return recommendations



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)