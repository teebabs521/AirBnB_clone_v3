#!/usr/bin/python3
"""Blueprint for API views"""

from flask import Blueprint

# Create Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes (PEP8 will complain, but ignore)
from api.v1.views.index import *  # Index view for the API

# Import the views for the different objects
from api.v1.views.states import app_views as states_views
from api.v1.views.cities import *  # Cities routes
from api.v1.views.amenities import *  # Amenities routes
from api.v1.views.users import *  # Users routes
from api.v1.views.places import *  # Import places views
from api.v1.views.places_reviews import *  # Import places reviews views


# Register the blueprint for states
app_views.register(states_views)

