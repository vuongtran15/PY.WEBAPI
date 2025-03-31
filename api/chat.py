
from fastapi import HTTPException
import fastapi
from pydantic import BaseModel
from services.aidb_services import AIDBContext

router = fastapi.FastAPI()


class ConversationByEmpIdRequest(BaseModel):
    emp_id: str

@router.post("/conversation/byempid")
async def get_conversation_by_empid(request: ConversationByEmpIdRequest):
    db_context = AIDBContext()
    
    # Fetch conversation details from the database
    conversations = db_context.load_conversation_by_empid(request.emp_id)
    
    if not conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations