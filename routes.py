"""
routes.py - Defines API routes for Flask app.

This script contains the RESTful API endpoints for
retrieving and inserting sales data into the database.
It interacts with db.py to execute queries.

Author: Luke Thurston
Date: 3/15/25

"""

from flask import Blueprint, request, jsonify
from db import execute_query

import pandas as pd

sales_blueprint = Blueprint('sales', __name__)

# 1. View all Sales Records
@sales_blueprint.route('/sales', methods=['GET'])
def get_sales():
    query = "SELECT * FROM Sales ORDER BY id ASC"
    sales = execute_query(query, fetch=True)
    return jsonify(sales)

# 2. Add a Sales Record
@sales_blueprint.route('/sales', methods=['POST'])
def add_sale():
    data = request.json
    query = "INSERT IGNORE INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)"
    execute_query(query, (data['store_code'], data['total_sale'], data['transaction_date']))
    return jsonify({"message": "Sale added successfully"}), 201

# 3. Return Records in a Date Range
@sales_blueprint.route('/sales/date-range', methods=['GET'])
def get_sales_by_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date parameters are required"}), 400
    
    query = "SELECT * FROM Sales WHERE transaction_date BETWEEN %s AND %s ORDER BY transaction_date ASC"
    sales = execute_query(query, (start_date, end_date), fetch=True)
    
    sales_list = [list(sale.values()) for sale in sales]
    sales_df = pd.DataFrame(sales)
    
    return jsonify({
        "json_dict": sales,
        "list": sales_list,
        "pandas_dataframe": sales_df.to_dict(orient='records')
    })

# 4. Add Sales Record with Verification
@sales_blueprint.route('/sales/add', methods=['POST'])
def add_new_sale():
    data = request.json
    
    required_fields = ["id", "store_code", "total_sale", "transaction_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id, store_code, total_sale, transaction_date"}), 400
    
    query = "INSERT INTO Sales (id, store_code, total_sale, transaction_date) VALUES (%s, %s, %s, %s)"
    execute_query(query, (data['id'], data['store_code'], data['total_sale'], data['transaction_date']))
    
    # Verify the inserted row
    verify_query = "SELECT * FROM Sales WHERE id = %s"
    inserted_row = execute_query(verify_query, (data['id'],), fetch=True)
    
    return jsonify({
        "message": "Sale added successfully",
        "inserted_data": inserted_row
    }), 201