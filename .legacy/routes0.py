from flask import Blueprint, request, jsonify
from db import execute_query

sales_blueprint = Blueprint('sales', __name__)

@sales_blueprint.route('/sales', methods=['GET'])
def get_sales():
    query = "SELECT * FROM Sales ORDER BY id ASC"
    sales = execute_query(query, fetch=True)
    return jsonify(sales)

@sales_blueprint.route('/sales', methods=['POST'])
def add_sale():
    data = request.json
    query = "INSERT IGNORE INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)"
    execute_query(query, (data['store_code'], data['total_sale'], data['transaction_date']))
    return jsonify({"message": "Sale added successfully"}), 201