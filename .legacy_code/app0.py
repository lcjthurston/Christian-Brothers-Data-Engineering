from flask import Flask, request, jsonify
import mysql.connector, re, csv

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "StoreData"
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

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

# Create database and table
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
            transaction_date DATE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Load data from CSV
def load_data_from_csv(csv_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_sale = float(re.sub(r'[^0-9.]', '', row['total_sale']))  # Remove '$' and convert to float
            cursor.execute("INSERT INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)", 
                           (row['store_code'], total_sale, row['transaction_date']))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/sales', methods=['GET'])
def get_sales():
    query = "SELECT * FROM Sales"
    sales = execute_query(query, fetch=True)
    return jsonify(sales)

@app.route('/sales', methods=['POST'])
def add_sale():
    data = request.json
    total_sale = float(re.sub(r'[^0-9.]', '', data['total_sale']))  # Remove '$' and convert to float
    query = "INSERT INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)"
    execute_query(query, (data['store_code'], total_sale, data['transaction_date']))
    return jsonify({"message": "Sale added successfully"}), 201

if __name__ == '__main__':
    setup_database()
    load_data_from_csv("MOCK_DATA.csv")  # Ensure the file is placed in the same directory
    app.run(debug=True)
