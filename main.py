from fastapi import Depends, FastAPI, HTTPException
from routes.UserRoutes import router as user_router
from routes.LoginRoutes import router as login_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router,prefix='/api',tags=['Users'])
app.include_router(login_router,prefix='/api',tags=['Login/Signup'])

@app.get("/")
async def root():
    return {"message": "Welcome to User API"}