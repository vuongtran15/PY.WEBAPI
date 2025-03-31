import pyodbc
from fastapi import HTTPException

def get_db_connection():
    # Database connection function for common use
    conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=172.19.18.58;Database=AIDB;UID=ros;PWD=*123qwe*;Encrypt=YES;TrustServerCertificate=YES;"
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
