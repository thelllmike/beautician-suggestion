# Beautician Recommendation System

This project is a Beautician Recommendation System built using FastAPI and a pre-trained BERT model. The system uses sentiment analysis and user preferences to recommend the best beauticians based on their reviews.


### Explanation:

- **Project Title and Description**: A brief overview of what the project does.
- **Features**: Highlights the main features of the project.
- **Installation**: Step-by-step instructions to set up the project locally.
- **Usage**: Instructions on how to run the FastAPI server and use the API.
- **API Endpoints**: Detailed information about the API endpoint including request body and example.
- **Contributing**: A note encouraging contributions.
- **License**: Information about the project’s license.

This README template provides a comprehensive guide for users to understand, set up, and use your project. Adjust the paths and repository details as necessary.


## Features

- Sentiment analysis of beautician reviews using a pre-trained BERT model.
- Customizable recommendations based on user preferences.
- FastAPI backend to handle requests and return recommendations.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thelllmike/beautician-suggestion.git
   cd beautician-recommendation-system


BACKEND
│
├── crud
│   ├── __pycache__
│   ├── __init__.py
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
│   ├── __pycache__
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
│   ├── __pycache__
│   ├── __init__.py
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
    ├── __pycache__
    ├── __init__.py
    ├── admin_schema.py
    ├── appointments_schema.py
    ├── beautician_schema.py
    ├── customer_schema.py
    ├── preferences_schema.py
    ├── review_schema.py
    ├── salon_schema.py
    └── visuals_schema.py

