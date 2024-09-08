# database.py

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/saloon"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# Assuming you are doing this in a Python environment
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# Credentials and configuration
username = 'adming'  # Adjust as needed
password = urllib.parse.quote_plus('Research@glowup')  # URL encode the password if it contains special characters
host = 'glowupdb.mysql.database.azure.com'
database = 'saloon'

# Connection string
DATABASE_URL = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"

# Engine configuration
engine = create_engine(DATABASE_URL, echo=True, pool_size=10, max_overflow=20)

# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative class
Base = declarative_base()
