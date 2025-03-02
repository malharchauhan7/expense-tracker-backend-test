from fastapi import APIRouter, HTTPException
from models.UserModel import User
from typing import Dict
from pydantic import BaseModel
from controllers.UserController import login_user,create_user

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

class SignupData(BaseModel):
    name: str
    email: str
    password: str
    status: bool = True
    isAdmin: bool = False

@router.post("/login", response_model=Dict)
async def login(login_data: LoginData):
    return await login_user(login_data.email, login_data.password)

@router.post("/signup", response_model=Dict)
async def signup(signup_data: SignupData):
    # Convert SignupData to User model
    user = User(**signup_data.model_dump())
    return await create_user(user)