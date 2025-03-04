from pydantic import BaseModel,Field, field_validator
from datetime import datetime
from typing import Optional
import bcrypt

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    password: str
    isAdmin: bool=False
    status: bool
    updated_at: Optional[int] = None
    created_at: Optional[int] = None

    @field_validator('password')
    def hash_password(cls,password:str)->str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
        return hashed.decode('utf-8')
    
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )