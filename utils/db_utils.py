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

def execute_query_none_retrun(conn, query, params=None):
    # Execute a query that does not return any data (e.g., INSERT, UPDATE, DELETE)
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def execute_query_return(conn, query, params=None):
    # Execute a query that returns data (e.g., SELECT)
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def execute_query_return_one(conn, query, params=None):
    # Execute a query that returns a single row of data
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")
    finally:
        cursor.close()
        conn.close()