#!/usr/bin/python3
"""Blueprint for API views"""

from flask import Blueprint

# Create Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes (PEP8 will complain, but ignore)
from api.v1.views.index import *

