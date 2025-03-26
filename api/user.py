import fastapi
from fastapi import HTTPException, Depends
from pydantic import BaseModel
from utils.db_utils import get_db_connection

router = fastapi.APIRouter()

# Define login request model
class LoginRequest(BaseModel):
    emp_id: str
    password: str

@router.post("/login")
async def login(login_data: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Query to check if the employee exists with the provided credentials
        query = "SELECT Emp_id FROM employee WHERE Emp_id = ? AND [Password] = ?"
        cursor.execute(query, (login_data.emp_id, login_data.password))
        
        user = cursor.fetchone()
        
        if user:
            return {"message": "Login successful", "emp_id": user[0]}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# Keep the original GET endpoint for backward compatibility
@router.get("/login")
async def login_get():
    return {"message": "Hello World1"}
