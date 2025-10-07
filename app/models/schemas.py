from pydantic import BaseModel
from typing import Dict, Any, Optional

# Model untuk data yang diterima dari request POST /mine
class TransactionInput(BaseModel):
    user_id: str
    action: str  # e.g., "register", "post_photo"
    post_id: Optional[str] = None
    

# Model untuk response yang lebih terstruktur (opsional tapi disarankan)
class BlockResponse(BaseModel):
    message: str
    block: Dict[str, Any]

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    id: str
    name: str
    email: str
