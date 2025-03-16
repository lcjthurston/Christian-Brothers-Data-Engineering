"""
db.py - Handles database connection and setup.

This script configures the MySQL database connection,
executes queries, and ensures the necessary tables
are created.

Author: Luke Thurston
Date: 3/15/25

"""

import mysql.connector

# 1. Database Configuration Dict.
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "68P<h<v7!,*6",
    "database": "StoreData"
}

# 2. Function to Return Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 3. Function to run MySQL Queries
def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    
    result = cursor.fetchall() if fetch else None
    conn.commit()
    
    cursor.close()
    conn.close()
    return result

# 4. Create Database and Table
def setup_database():
    conn = get_db_connection()
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
        )
    """)
    
    cursor.execute("ALTER TABLE Sales AUTO_INCREMENT = 1")
    conn.commit()
    
    cursor.close()
    conn.close()

