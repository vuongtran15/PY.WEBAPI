
from utils.db_utils import get_db_connection

class AIDBContext:
    def __init__(self):
        self.db = get_db_connection()
    
    def insert_conversation(self, id, emp_id, title, conversation_type):
        """
        Insert a new conversation with the given ID if it doesn't exist.
        
        Args:
            id (int): The ID to use for the conversation
            emp_id (str): Employee ID
            title (str): Conversation title
            conversation_type (str): Type of conversation
            
        Returns:
            int: The ID of the inserted or existing conversation
        """
        cursor = self.db.cursor()
        
        # Check if conversation exists
        cursor.execute(
            "SELECT Id FROM [AIDB].[dbo].[AI_Conversation] WHERE EmpId = ? AND Title = ? AND IsDeleted = 0",
            (emp_id, title)
        )
        result = cursor.fetchone()
        
        if result:
            return result[0]
        
        # Insert new conversation with specified ID
        cursor.execute(
            """
            INSERT INTO [AIDB].[dbo].[AI_Conversation] 
            (Id, EmpId, CreatedAt, Title, Type, IsDeleted)
            VALUES (?, ?, GETDATE(), ?, ?, 0);
            """,
            (id, emp_id, title, conversation_type)
        )
        
        self.db.commit()
        return id

def insert_conversation_detail(self, id, conversation_id, sender_type, data_type, message_text):
    """
    Insert a new conversation detail with the given ID and update conversation title if empty.
    
    Args:
        id (int): The ID to use for the conversation detail
        conversation_id (int): ID of the parent conversation
        sender_type (str): Type of sender (e.g., 'user', 'assistant')
        data_type (str): Type of data (e.g., 'text', 'image')
        message_text (str): Content of the message
        
    Returns:
        int: The ID of the inserted conversation detail
    """
    cursor = self.db.cursor()
    
    # Insert the conversation detail with specified ID
    cursor.execute(
        """
        INSERT INTO [AIDB].[dbo].[AI_ConversationDetail]
        (Id, ConversationId, SenderType, CreatedAt, DataType, MessageText)
        VALUES (?, ?, ?, GETDATE(), ?, ?);
        """,
        (id, conversation_id, sender_type, data_type, message_text)
    )
    
    # Check if the parent conversation title is empty and update if needed
    if sender_type == 'user':
        cursor.execute(
            """
            UPDATE [AIDB].[dbo].[AI_Conversation]
            SET Title = ?
            WHERE Id = ? AND (Title IS NULL OR LTRIM(RTRIM(Title)) = N'New Conversation')
            """,
            (message_text[:50] if len(message_text) > 50 else message_text, conversation_id)
        )
    
    self.db.commit()
    return id

#load conversation by empid

def load_conversation_by_empid(self, emp_id):
    """
    Load conversations for a specific employee ID.
    
    Args:
        emp_id (str): Employee ID
        
    Returns:
        list: List of conversations for the specified employee ID
    """
    cursor = self.db.cursor()
    
    cursor.execute(
        """
        SELECT Id, EmpId, CreatedAt, Title, Type
        FROM [AIDB].[dbo].[AI_Conversation]
        WHERE EmpId = ? AND IsDeleted = 0
        """,
        (emp_id,)
    )
    
    return cursor.fetchall()