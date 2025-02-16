#!/usr/bin/python3
"""Blueprint for API views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all views (even though PEP8 will complain)
from api.v1.views.index import *

