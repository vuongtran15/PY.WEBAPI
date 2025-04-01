
import datetime
import pydoc
from typing import Any
import fastapi
from fastapi import HTTPException
from pydantic import BaseModel


from services.aidb_services import AIDBContext

router = fastapi.APIRouter()


class ConversationByEmpIdRequest(BaseModel):
    emp_id: str

def make_json_serializable(value: Any) -> Any:
    """Convert non-JSON-serializable values to a compatible format."""
    if isinstance(value, datetime):
        return value.isoformat()  # Convert datetime to ISO 8601 string
    elif value is None:
        return None
    elif isinstance(value, (int, float, str, bool)):
        return value
    elif isinstance(value, (list, tuple)):
        return [make_json_serializable(item) for item in value]
    elif isinstance(value, dict):
        return {k: make_json_serializable(v) for k, v in value.items()}
    else:
        return str(value)  # Fallback: convert unknown types to string

@router.post("/conversation/byempid")
async def get_conversation_by_empid(request: ConversationByEmpIdRequest):
    db_context = AIDBContext()
        
    # Fetch conversation details from the database
    conversations_raw = db_context.load_conversation_by_empid(request.emp_id)

    if not conversations_raw:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversations = []
    try:
        for conv in conversations_raw:
            if isinstance(conv, dict):
                # If it's already a dict, ensure all values are serializable
                conv_dict = {k: make_json_serializable(v) for k, v in conv.items()}
                conversations.append(conv_dict)
            elif isinstance(conv, pydoc.Row):
                # Convert pyodbc.Row to a dictionary and ensure serializability
                conv_dict = dict(zip([col[0] for col in conv.cursor_description], conv))
                conv_dict = {k: make_json_serializable(v) for k, v in conv_dict.items()}
                conversations.append(conv_dict)
            elif hasattr(conv, '__dict__'):
                # If it's an object with __dict__
                conv_dict = {k: make_json_serializable(v) for k, v in vars(conv).items()}
                conversations.append(conv_dict)
            elif isinstance(conv, (tuple, list)):
                # If it's a tuple/list, map to a dict (adjust fields as needed)
                conv_dict = {
                    "id": make_json_serializable(conv[0]),
                    "message": make_json_serializable(conv[1]),
                    "timestamp": make_json_serializable(conv[2])
                }
                conversations.append(conv_dict)
            else:
                raise ValueError(f"Unsupported conversation data type: {type(conv)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing conversation data: {str(e)}")
    
    return conversations