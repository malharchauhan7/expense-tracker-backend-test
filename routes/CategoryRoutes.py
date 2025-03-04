from fastapi import APIRouter, HTTPException
from controllers.CategoryController import get_all_categories,get_category_by_id,create_category,update_category_by_id,delete_category_by_id
from models.CategoryModel import Category

router = APIRouter()

# Get All categories
@router.get('/category')
async def read_category():
    return await get_all_categories()

# Get Category by Id
@router.get('/category/{category_id}')
async def read_category_by_id(category_id:str):
    category = await get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category not found")
    return category

# Create Category
@router.post("/category")
async def createcategory(category:Category):
    return await create_category(category)

# Update Category by Id
@router.put("/category/{category_id}")
async def update_category(category_id:str,category:Category):
    return await update_category_by_id(category_id,category)

# Delete Category by Id
@router.delete("/category/{category_id}")
async def delete_category(category_id:str):
    return await delete_category_by_id(category_id)