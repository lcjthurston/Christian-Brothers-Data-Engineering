"""
app.py - Main entry point for Flask app.

This script initializes our app, sets up the database,
and registers API routes. It ensures that the database
and tables are properly created before running the server.

Author: Luke Thurston
Date: 3/15/25

"""

from flask import Flask

from db import setup_database
from routes import sales_blueprint
from utils import load_data_from_excel

app = Flask(__name__)

setup_database()

app.register_blueprint(sales_blueprint)

load_data_from_excel("MOCK_DATA.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
