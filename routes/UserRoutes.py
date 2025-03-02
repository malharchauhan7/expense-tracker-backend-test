from fastapi import APIRouter, HTTPException
from controllers.UserController import get_user,get_user_by_id,create_user,updated_user_by_id,delete_user_by_id
from models.UserModel import User

router = APIRouter()

@router.get("/users")
async def read_user():
    return await get_user()

@router.get("/users/{user_id}")
async def read_user_by_id(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users")
async def createuser(user: User):
    return await create_user(user)

@router.put('/users/{user_id}')
async def update_user(user_id:str,user:User):
    return await updated_user_by_id(user_id,user)

@router.delete("/users/{user_id}")
async def delete_user(user_id:str):
    return await delete_user_by_id(user_id)