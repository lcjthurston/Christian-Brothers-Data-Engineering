from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd

app = Flask(__name__)

global_var = False

# 1. Database Configuration

# a. Dictionary of Config Info
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "68P<h<v7!,*6",
    "database": "StoreData"
}

# b. Function to Return Connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# c. Function to run MySQL Query
def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    if fetch:
        result = cursor.fetchall()
    else:
        conn.commit()
        result = None
    
    cursor.close()
    conn.close()
    return result

# 2. Create database and table
def setup_database():
    conn = mysql.connector.connect(host=db_config["host"], user=db_config["user"], password=db_config["password"])
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS StoreData")
    conn.database = "StoreData"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            store_code VARCHAR(10),
            total_sale DECIMAL(10,2),
            transaction_date DATE,
            CONSTRAINT unique_sales_entry UNIQUE (store_code, total_sale, transaction_date)
        ) AUTO_INCREMENT = 1
    """)
    conn.commit()
    cursor.execute("ALTER TABLE Sales AUTO_INCREMENT = 1")
    conn.commit()
    cursor.close()
    conn.close()

# 3. Load data from Excel
def load_data_from_excel(excel_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    df = pd.read_excel(excel_path)
    global global_var
    if (global_var == False):
        for _, row in df.iterrows():
            cursor.execute("INSERT IGNORE INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)", 
                           (row['store_code'], row['total_sale'], row['transaction_date']))
        global_var = True
    conn.commit()
    cursor.close()
    conn.close()

# 4. App Endpoints w. Modular Blueprints
@app.route('/sales', methods=['GET'])
def get_sales():
    query = "SELECT * FROM Sales ORDER BY id ASC"
    sales = execute_query(query, fetch=True)
    return jsonify(sales)

@app.route('/add_sales', methods=['POST'])
def add_sale():
    data = request.json
    query = "INSERT IGNORE INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)"
    execute_query(query, (data['store_code'], data['total_sale'], data['transaction_date']))
    return jsonify({"message": "Sale added successfully"}), 201

# 5. Server Execution
if __name__ == '__main__':
    setup_database()
    load_data_from_excel("MOCK_DATA.xlsx")
    app.run(debug=True)