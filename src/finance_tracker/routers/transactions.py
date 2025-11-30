from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timezone

from ..database import get_db
from ..models import Transaction, Category, TransactionType, User
from ..schemas import TransactionCreate, TransactionUpdate, TransactionResponse
from ..auth import get_current_user

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"]
)


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    start_date: Optional[datetime] = Query(None, description="Filter transactions from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter transactions until this date"),
    transaction_type: Optional[TransactionType] = Query(None, description="Filter by transaction type"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of transactions with optional filtering and pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **start_date**: Filter transactions from this date (ISO format)
    - **end_date**: Filter transactions until this date (ISO format)
    - **transaction_type**: Filter by type (income or expense)
    - **category_id**: Filter by category ID
    """
    # Build query - filter by current user
    query = select(Transaction).where(Transaction.user_id == current_user.id)
    
    # Apply filters
    if start_date:
        query = query.where(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.where(Transaction.transaction_date <= end_date)
    if transaction_type:
        query = query.where(Transaction.type == transaction_type)
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    
    # Order by transaction date (newest first) and apply pagination
    query = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific transaction by ID.
    """
    query = select(Transaction).where(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    )
    
    result = await db.execute(query)
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new transaction.
    
    - **amount**: Transaction amount (must be greater than 0)
    - **type**: Transaction type (income or expense)
    - **transaction_date**: Date of the transaction (defaults to now if not provided)
    - **description**: Optional description
    - **category_id**: Optional category ID
    """
    # Validate category if provided (must belong to current user)
    if transaction_data.category_id:
        category_query = select(Category).where(
            and_(Category.id == transaction_data.category_id, Category.user_id == current_user.id)
        )
        
        category_result = await db.execute(category_query)
        category = category_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or does not belong to you"
            )
    
    # Create transaction for current user
    new_transaction = Transaction(
        amount=transaction_data.amount,
        type=transaction_data.type,
        description=transaction_data.description,
        category_id=transaction_data.category_id,
        transaction_date=transaction_data.transaction_date or datetime.now(timezone.utc),
        user_id=current_user.id
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing transaction.
    
    Only provided fields will be updated (partial update).
    """
    # Get transaction (must belong to current user)
    query = select(Transaction).where(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    )
    
    result = await db.execute(query)
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Validate category if being updated (must belong to current user)
    if transaction_data.category_id is not None:
        category_query = select(Category).where(
            and_(Category.id == transaction_data.category_id, Category.user_id == current_user.id)
        )
        
        category_result = await db.execute(category_query)
        category = category_result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or does not belong to you"
            )
    
    # Update fields (only provided fields)
    update_data = transaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    await db.commit()
    await db.refresh(transaction)
    
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a transaction.
    """
    # Get transaction for the current user
    query = select(Transaction).where(
        and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    )
    
    result = await db.execute(query)
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    await db.delete(transaction)
    await db.commit()
    
    return None
