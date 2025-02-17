#!/usr/bin/python3
"""Flask Application for API"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(app_views)

# Close storage when request ends
@app.teardown_appcontext
def close_storage(exception):
    """Calls storage.close()"""
    storage.close()

if __name__ == "__main__":
    # Get environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    
    # Run Flask app
    app.run(host=host, port=port, threaded=True)


#!/usr/bin/python3
"""Flask Application for API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(app_views)

# Close storage when request ends
@app.teardown_appcontext
def close_storage(exception):
    """Calls storage.close()"""
    storage.close()

# 404 Error Handler
@app.errorhandler(404)
def not_found(error):
    """Returns a JSON response for 404 errors"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Get environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    
    # Run Flask app
    app.run(host=host, port=port, threaded=True)

