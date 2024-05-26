from flask import Flask
from flask_cors import CORS
import os
from data import get_data, opendb, update_db

app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) for all routes
CORS(app)

# Get secret key from environment variable
secret = os.environ.get('SECRET_KEY')


# Route to fetch data
@app.route('/api/data', methods=['GET'])
def data():
    """
    Route handler to fetch data from the database.

    Returns:
        JSON response containing fetched data.
    """
    return get_data(secret)


# Route to update data
@app.route('/api/update', methods=['POST'])
def update():
    """
    Route handler to update data in the database.

    Returns:
        None
    """
    update_db(secret)


# Run the Flask app
if __name__ == '__main__':
    # Open database connection before starting the app
    opendb(secret)
    # Run the app in debug mode on all interfaces at port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
