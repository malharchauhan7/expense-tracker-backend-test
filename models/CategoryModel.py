from pydantic import BaseModel,Field, field_validator
from datetime import datetime
from typing import Optional,Dict,Any
from bson import ObjectId

class Category(BaseModel):
    id: Optional[str] = Field(alias="_id") 
    user_id: Optional[str] = None
    name:str
    status:Optional[bool]=True
    updated_at: Optional[int] = None
    created_at: Optional[int] = None

# class CategoryOut(Category):
#     id:str = Field(alias="_id") 
    
#     @field_validator('id',mode="before")
#     def convert_objectId(cls,v):
#         if isinstance(v,ObjectId):
#             return str(v)
#         return v
    
#     @field_validator('user_id',mode="before")
#     def convert_userid(cls,v):
#         if isinstance(v,dict) and "_id" in v:
#             v["_id"] = str(v["_id"])
#         return v