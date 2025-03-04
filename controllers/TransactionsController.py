from bson import ObjectId
from config.db import category_collection,users_collection,transactions_collection
from models.TransactionsModel import Transaction
from datetime import datetime,UTC
from fastapi import HTTPException


def Transaction_Out(transaction):
    return {
        "_id":str(transaction["_id"]),
        "user_id":transaction["user_id"],
        "category_id":transaction["category_id"],
        "transaction_type":transaction["transaction_type"],
        "amount":transaction["amount"],
        "description":transaction["description"],
        "date":transaction["date"],
        "status":transaction["status"],
        "updated_at": transaction["updated_at"],
        "created_at": transaction["created_at"],
    }
    
# Get All Transactions
async def get_all_transations():
    try:
        transactions = await transactions_collection.find().to_list(length=None)
        
        for transaction in transactions:
            if ( "user_id" in transaction and isinstance(transaction["user_id"],ObjectId) ) and ("category_id" in transaction and isinstance(transaction["category_id"],ObjectId)):
                user["user_id"] = str(transaction["user_id"])
                category["category_id"] = str(transaction["category_id"])
                
            user = await users_collection.find_one({"_id":ObjectId(transaction["user_id"])})
            category = await category_collection.find_one({"_id":ObjectId(transaction["category_id"])})
            
            if user and category:
                user["_id"] = str(user["_id"])
                transaction["user_id"] = user
                category["_id"] = str(category["_id"])
                transaction["category_id"] = category
            
        if not transactions:
            raise HTTPException(status_code=404,detail="No Transactions Found")
            
        return [Transaction_Out(transaction) for transaction in transactions]
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error:{str(e)}")
    

# Get Transaction by Id
async def get_transaction_by_id(transaction_id:str):
    try:
        transaction = await transactions_collection.find_one({"_id":ObjectId(transaction_id)})
        
        if not transaction:
            raise HTTPException(status_code=404,detail="No Transaction found")
        
        if ( "user_id" in transaction and isinstance(transaction["user_id"],ObjectId) ) and ("category_id" in transaction and isinstance(transaction["category_id"],ObjectId)):
                user["user_id"] = str(transaction["user_id"])
                category["category_id"] = str(transaction["category_id"])
                
        user = await users_collection.find_one({"_id":ObjectId(transaction["user_id"])})
        category = await category_collection.find_one({"_id":ObjectId(transaction["category_id"])})
            
        if user and category:
            user["_id"] = str(user["_id"])
            transaction["user_id"] = user
            category["_id"] = str(category["_id"])
            transaction["category_id"] = category
        
        return Transaction_Out(transaction)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error:{str(e)}")
    
    
# Create a Transaction 
async def create_transaction(transaction:Transaction):
    try:
        current_time = datetime.now(UTC)
        
        new_transaction = transaction.model_dump(exclude={"id"})
        new_transaction.update({
            "created_at": current_time,
            "updated_at": current_time,
            "date":current_time
        })
        
        inserted_transaction = await transactions_collection.insert_one(new_transaction)
        
        if not inserted_transaction.inserted_id:
            raise HTTPException(status_code=404,detail="Failed to create transaction")
        
        return await get_transaction_by_id(str(inserted_transaction.inserted_id))
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error: {str(e)}")
    
# Update a Transaction
async def update_transaction_by_id(transaction_id:str,transaction:Transaction):
    try:    
        existring_transaction = await get_transaction_by_id(transaction_id)
        if not existring_transaction:
            raise HTTPException(status_code=404,detail="No Transaction Found")
        
        update_data = {
            key: value for key, value in transaction.model_dump(
                exclude={"id"}, 
                exclude_unset=True
            ).items()
        }
        
        if not update_data:
            return existring_transaction
        
        update_data["updated_at"] = datetime.now(UTC)
        
        result = await transactions_collection.update_one({"_id":ObjectId(transaction_id)},{"$set":update_data})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400,detail="Update Operation Failed")
        
        return await get_transaction_by_id(transaction_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    
    
# Delete Transaction by Id
async def delete_transaction_by_id(transaction_id:str):
    try:
        existing_transaction = await get_transaction_by_id(transaction_id)
        if not existing_transaction:
            raise HTTPException(status_code=404,detail="Transaction Not Found")
        
        await transactions_collection.delete_one({"_id":ObjectId(transaction_id)})
        
        return {"message":"Transaction Deleted Successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")