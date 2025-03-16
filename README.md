# Christian Brothers Data Engineering

## Overview
This project is a Flask-based REST API that connects to a MySQL database, providing CRUD operations for managing sales data. The application loads sales data from an Excel file into the database and supports operations such as retrieving, adding, and filtering sales records by date range.

## Features
- RESTful API using Flask
- MySQL database for data persistence
- Excel data ingestion
- Retrieve all sales records
- Query sales data within a date range
- Insert new sales records
- Duplicate prevention using unique constraints

## Project Structure
```
/flask_app
│── app.py              # Main application file (initializes Flask app)
│── db.py               # Database connection & setup
│── routes.py           # API route definitions
│── utils.py            # Utility functions for Excel data loading
│── requirements.txt    # Dependencies
│── MOCK_DATA.xlsx      # Sample sales data
│── README.md           # Project documentation
```

## Note
To replicate this code on your own machine it's important to install MySQL Server and create a 
schema named `storedata` in MySQL Workbench.

## Setup Instructions
### 1. Install Dependencies
Ensure you have Python installed. Then, install the required dependencies:
```sh
pip install -r requirements.txt
```

### 2. Configure MySQL Database
Ensure MySQL Server is running. Update the `db_config` in `db.py` with your credentials:
```python
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "StoreData"
}
```

### 3. Run the Application
Start the Flask server:
```sh
python app.py
```

### 4. API Endpoints
#### Retrieve All Sales Records
```http
GET /sales
```
#### Retrieve Sales Data by Date Range
```http
GET /sales/date-range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
#### Insert a New Sale Record
```http
POST /sales/add
Content-Type: application/json

{
    "id": 1001,
    "store_code": "TX001",
    "total_sale": 100.00,
    "transaction_date": "2023-01-20"
}
```

### 5. Testing Endpoints
To ensure that this application works as expected it's necessary to test the endpoints with real data.
I recommend testing with an API development platform such as Postman or Insomnia. To view the results 
of my tests please examine the `testing_imgs` folder above.

## Author
Luke Thurston

