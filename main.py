from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
from textblob import TextBlob

# Define the data model for incoming requests
class Review(BaseModel):
    name: str
    review: str

class Preference(BaseModel):
    style: List[str]
    interaction: List[str]
    speed: List[str]
    personality: List[str]
    average_time: List[str]

# Initialize FastAPI app
app = FastAPI()

# Load the model and tokenizer
MODEL_PATH = 'path_to_save_model'
TOKENIZER_PATH = 'path_to_save_tokenizer'
tokenizer = BertTokenizer.from_pretrained(TOKENIZER_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Function to predict sentiment
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
    sentiment_score = torch.softmax(logits, dim=1)[:, 1].item()  # Assuming class 1 is positive
    return sentiment_score

# Route to analyze and recommend beauticians
@app.post("/recommend/")
async def recommend_beauticians(reviews: List[Review], preferences: Preference):
    beauticians = pd.DataFrame([review.dict() for review in reviews])
    beauticians['sentiment_score'] = beauticians['review'].apply(predict_sentiment)

    # Calculate scores based on sentiment and preferences
    def score_beautician(row):
        score = row['sentiment_score'] * 10  # Scale up sentiment score
        review_text = row['review'].lower()
        for pref, keywords in preferences.dict().items():
            if any(keyword in review_text for keyword in keywords):
                score += 1
        return score

    beauticians['score'] = beauticians.apply(score_beautician, axis=1)
    recommended = beauticians.sort_values(by='score', ascending=False)
    return recommended[['name', 'score']].to_dict(orient='records')

