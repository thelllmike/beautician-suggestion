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

# Hardcoded reviews
hardcoded_reviews = [
    {"name": "Rami", "review": "Rami provided an excellent service with a modern haircut that was quick and professional. Highly recommended!"},
    {"name": "Madushanka", "review": "Madushanka's work on traditional makeup wasn't up to par this time, lacked the usual charm."},
    {"name": "Manoj", "review": "Manoj was quite informative and friendly while providing a quick and efficient haircut. Very happy with the results!"},
    {"name": "Sasha", "review": "Sasha’s work was disciplined but too slow, and the support was lacking during the long session."}
]

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
async def recommend_beauticians(preferences: Preference):
    # Convert hardcoded reviews to DataFrame
    beauticians = pd.DataFrame(hardcoded_reviews)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
