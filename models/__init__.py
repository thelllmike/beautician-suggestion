from .admin_model import Admin
from .beautician_model import Beautician
from .salon_model import Salon
from .customer_model import Customer
from .preferences_model import Preferences
from .appointments_model import Appointments
from .review_model import Review
from .visuals_model import SalonVisuals

# Import Base and engine from the database module
from database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)
