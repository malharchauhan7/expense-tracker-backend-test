from bson import ObjectId
from config.db import users_collection
from models.UserModel import User
from datetime import datetime,UTC
from fastapi import HTTPException
from pymongo.errors import PyMongoError

# Helper Function to format MongoDB Doc
def user_serializer(user):
    return {
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "isAdmin": user["isAdmin"],
        "status": user["status"],
        "updated_at": user["updated_at"],
        "created_at": user["created_at"],
    }

# Get all users
async def get_user():
    try:
        users =  users_collection.find().to_list(length=None)
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return [user_serializer(user) for user in users]
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# Get user by ID
async def get_user_by_id(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user_serializer(user)
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# Create a User
async def create_user(user: User):
    try:
        # Check if user already exists
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        current_time = datetime.now(UTC)
        new_user = user.model_dump(exclude={"id"})
        new_user.update({
            "created_at": current_time,
            "updated_at": current_time
        })
        
        inserted_user = users_collection.insert_one(new_user)
        
        if not inserted_user.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to create user")
            
        return await get_user_by_id(str(inserted_user.inserted_id))
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# Update User by Id 
async def updated_user_by_id(user_id: str, user: User):
    try:
        existing_user = await get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User Not Found")
        
        
        update_data = {
            key: value for key, value in user.model_dump(exclude={"id"}).items()
            if value is not None
        }
        
        if not update_data:  
            return existing_user
        
        # Update the timestamp
        update_data["updated_at"] = datetime.now(UTC)

        # Perform the update
        result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Update operation failed")

        return await get_user_by_id(user_id)
    
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")   
    
# Delete User by Id
async def delete_user_by_id(user_id:str):
    try:
        existing_user = await get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404,detail="User Not Found")
        
        users_collection.delete_one({"_id":ObjectId(user_id)})
        return {"message":"User Deleted"}
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    
    
    
# Login User 

async def login_user(email: str, password: str):
    try:
        # Find user by email
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get stored hashed password
        stored_password = user.get("password")
        
        # Verify password
        if not User.verify_password(password, stored_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Return user data without password
        user_data = user_serializer(user)
        return user_data
        
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")