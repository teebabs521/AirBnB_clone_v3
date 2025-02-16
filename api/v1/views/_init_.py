#!/usr/bin/python3
"""Blueprint setup for API"""

from flask import Blueprint

# Define blueprint with prefix "/api/v1"
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes (wildcard import, PEP8 will complain but it's okay)
from api.v1.views.index import *

