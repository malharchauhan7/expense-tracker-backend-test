from bson import ObjectId
from config.db import category_collection,users_collection
from models.CategoryModel import Category
from datetime import datetime,UTC
from fastapi import HTTPException


def Category_Out(category):
    return {
        "_id":str(category["_id"]),
        "user_id":category["user_id"],
        "name":category["name"],
        "status":category["status"],
        "updated_at": category["updated_at"],
        "created_at": category["created_at"],
    }
    
    
# Get All Categories
async def get_all_categories():
    try:
        categories = await category_collection.find().to_list(length=None)
        
        for cat in categories:
            if "user_id" in cat and isinstance(cat["user_id"],ObjectId):
                user["user_id"] = str(cat["user_id"])
            
            user = await users_collection.find_one({"_id":ObjectId(cat["user_id"])})
            
            if user:
                user["_id"] = str(user["_id"])
                cat["user_id"] = user
        
        if not categories:
            raise HTTPException(status_code=404,detail="No Categories Found")
        return [Category_Out(cat) for cat in categories]
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error:{str(e)}")
    

# Get Category by Id
async def get_category_by_id(category_id:str):
    try:
        category = await category_collection.find_one({"_id":ObjectId(category_id)})
        if not category:
            raise HTTPException(status_code=404,detail="No Category Found")

        if "user_id" in category and isinstance(category["user_id"],ObjectId):
            category["user_id"] = str(category["user_id"])
        
        user = await users_collection.find_one({"_id":ObjectId(category["user_id"])})
        if user:
            user["_id"] = str(user["_id"])
            category["user_id"] = user
        
        return Category_Out(category)
        
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error:{str(e)}")
 
   
#Create a Category
async def create_category(category:Category):
    try:
        current_time = datetime.now(UTC)
    
        new_category = category.model_dump(exclude={"id"})
        new_category.update({
            "created_at": current_time,
            "updated_at": current_time
        })
        
        inserted_category = await category_collection.insert_one(new_category)
        
        if not inserted_category.inserted_id:
            raise HTTPException(status_code=400,detail="Failed to create category")
        
        return await get_category_by_id(str(inserted_category.inserted_id))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    
    
# Update Category by id
async def update_category_by_id(category_id:str,category:Category):
    try:

        existing_category = await get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404,detail="Category Not Found")
        
        update_data = {
            key: value for key, value in category.model_dump(exclude={"id"}).items()
            if value is not None
        }
        
        if not update_data:
            return existing_category
        
        update_data["updated_at"] = datetime.now(UTC)
        
        result = await category_collection.update_one({"_id":ObjectId(category_id)},{"$set":update_data})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400,detail="Update operation Failed")
        
        return await get_category_by_id(category_id)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    

# Delete Category by Id
async def delete_category_by_id(category_id:str):
    try:
        existing_category = await get_category_by_id(category_id)
        if not existing_category:
            raise HTTPException(status_code=404,detail="Category Not Found")
        
        await category_collection.delete_one({"_id":ObjectId(category_id)})
        
        return {"message":"Category Deleted Successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    