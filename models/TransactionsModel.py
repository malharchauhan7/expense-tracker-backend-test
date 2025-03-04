from pydantic import BaseModel,Field, field_validator
from typing import Optional
from datetime import datetime


class Transaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    category_id: str
    transaction_type: str
    amount: float
    description: Optional[str] = None
    date: Optional[datetime] = None
    status: Optional[bool] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    