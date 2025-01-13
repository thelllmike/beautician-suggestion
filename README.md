# Beautician Recommendation System

This project is a Beautician Recommendation System built using FastAPI and a pre-trained BERT model. The system uses sentiment analysis and user preferences to recommend the best beauticians based on their reviews.

---

## Features

- Sentiment analysis of beautician reviews using a pre-trained BERT model.
- Customizable recommendations based on user preferences.
- FastAPI backend to handle requests and return recommendations.

---

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thelllmike/beautician-suggestion.git
   cd beautician-recommendation-system
   ```

2. **Set up the backend environment:**
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

For a detailed walkthrough, watch the video tutorial below:

---

## Video Tutorial

[![Video Tutorial](https://img.youtube.com/vi/Yp8ikaL80qU/0.jpg)](https://www.youtube.com/watch?v=Yp8ikaL80qU)

---

## Usage

- Access the FastAPI Swagger UI for testing the endpoints at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Example Endpoint: `/recommendations`

- **Method**: `POST`
- **Description**: Provides beautician recommendations based on user input.
- **Request Body**:
  ```json
  {
      "user_preferences": ["Friendly staff", "Expert in hair care"],
      "minimum_rating": 4.5
  }
  ```
- **Response**:
  ```json
  {
      "recommendations": [
          {
              "beautician_name": "Jane Doe",
              "rating": 4.8,
              "specialties": ["Hair care", "Skincare"]
          },
          {
              "beautician_name": "John Smith",
              "rating": 4.7,
              "specialties": ["Makeup", "Nail art"]
          }
      ]
  }
  ```

---

## Directory Structure

```
BACKEND
│
├── crud
│   ├── admin_crud.py
│   ├── appointments_crud.py
│   ├── beautician_crud.py
│   ├── customer_crud.py
│   ├── preferences_crud.py
│   ├── review_crud.py
│   ├── salon_crud.py
│   └── visuals_crud.py
│
├── endpoints
│   ├── admin_router.py
│   ├── appointments_router.py
│   ├── beautician_router.py
│   ├── customer_router.py
│   ├── preferences_router.py
│   ├── review_router.py
│   ├── salon_router.py
│   └── visuals_router.py
│
├── models
│   ├── admin_model.py
│   ├── appointments_model.py
│   ├── beautician_model.py
│   ├── customer_model.py
│   ├── preferences_model.py
│   ├── review_model.py
│   ├── salon_model.py
│   └── visuals_model.py
│
└── schemas
    ├── admin_schema.py
    ├── appointments_schema.py
    ├── beautician_schema.py
    ├── customer_schema.py
    ├── preferences_schema.py
    ├── review_schema.py
    ├── salon_schema.py
    └── visuals_schema.py
```

---

## Contributing

We welcome contributions! Please follow the guidelines outlined in `CONTRIBUTING.md`.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
