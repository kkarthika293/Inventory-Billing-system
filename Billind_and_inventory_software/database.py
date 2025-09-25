# database.py

import mysql.connector
from mysql.connector import Error

# Function to connect to the MySQL database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",         # Your MySQL server (usually localhost)
            user="root",              # Your MySQL username
            password="Praveen@2930", # 🔁 Replace with your actual MySQL password
            database="billing_system"  # Your DB name
        )
        return connection
    except Error as e:
        print("❌ Database connection failed:", e)
        return None
