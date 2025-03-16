"""
utils.py - Flask App Helper functions.

Just one for this script - We need a utility function 
to load sales data from Excel. It helps maintain data 
integrity by preventing duplicates.

Author: Luke Thurston
Date: 3/15/25

"""

import pandas as pd
from db import get_db_connection

def load_data_from_excel(excel_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    df = pd.read_excel(excel_path)
    for _, row in df.iterrows():
        cursor.execute("INSERT IGNORE INTO Sales (store_code, total_sale, transaction_date) VALUES (%s, %s, %s)", 
                       (row['store_code'], row['total_sale'], row['transaction_date']))
    
    conn.commit()
    cursor.close()
    conn.close()