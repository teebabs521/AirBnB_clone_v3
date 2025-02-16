
etup for API"""

from flask import Blueprint

# Define blueprint with prefix "/api/v1"
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes (wildcard import, PEP8 will complain but it's okay)
from api.v1.views.index import *

etup for API"""

from flask import Blueprint

# Define blueprint with prefix "/api/v1"
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes (wildcard import, PEP8 will complain but it's okay)
from api.v1.views.index import *
 setup for AirBnB clone"""

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

