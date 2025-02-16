#!/usr/bin/python3
"""API setup for AirBnB clone"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register the app_views blueprint
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage session"""
    storage.close()

if __name__ == "__main__":
    # Get environment variables or set defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    # Run Flask application
    app.run(host=host, port=port, threaded=True)

