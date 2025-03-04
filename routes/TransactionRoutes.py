from fastapi import APIRouter,HTTPException
from controllers.TransactionsController import get_all_transations,get_transaction_by_id,create_transaction,update_transaction_by_id,delete_transaction_by_id
from models.TransactionsModel import Transaction

router = APIRouter()

# Get All Transactions
@router.get('/transactions')
async def read_transactions():
    return await get_all_transations()

@router.get("/transactions/{transaction_id}")
async def read_transaction_by_id(transaction_id:str):
    transaction = await get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404,detail="No Transaction found")
    
    return transaction

@router.post('/transactions')
async def create_Transaction(transaction:Transaction):
    return await create_transaction(transaction)

@router.put('/transactions/{transaction_id}')
async def update_transaction(transaction_id:str,transaction:Transaction):
    return await update_transaction_by_id(transaction_id,transaction)

@router.delete('/transactions/{transaction_id}')
async def delete_transaction(transaction_id:str):
    return await delete_transaction_by_id(transaction_id)