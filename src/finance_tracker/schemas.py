from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Dict
from .models import TransactionType


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserLogin(UserBase):
    """User login schema"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserResponse(UserBase):
    """User response schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# AUTHENTICATION SCHEMAS
# ============================================================================

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


# ============================================================================
# CATEGORY SCHEMAS
# ============================================================================

class CategoryBase(BaseModel):
    """Base category schema with common fields"""
    name: str = Field(..., min_length=3, max_length=50, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")


class CategoryCreate(CategoryBase):
    """Category creation schema"""
    pass  # Inherits all fields from CategoryBase


class CategoryUpdate(BaseModel):
    """Schema for updating a category (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")


class CategoryResponse(CategoryBase):
    """Category response schema"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# TRANSACTION SCHEMAS
# ============================================================================

class TransactionBase(BaseModel):
    """Base transaction schema with common fields"""
    amount: float = Field(..., gt=0, description="Transaction amount (must be greater than 0)")
    type: TransactionType = Field(..., description="Transaction type (income or expense)")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    category_id: Optional[int] = Field(None, description="Category ID (optional)")
    user_id: Optional[int] = Field(None, description="User ID (optional)")


class TransactionCreate(TransactionBase):
    """Transaction creation schema"""
    transaction_date: Optional[datetime] = Field(
        None,
        description="Transaction date (defaults to current time if not provided)"
    )

    


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction (all fields optional)"""
    amount: Optional[float] = Field(None, gt=0, description="Transaction amount")
    type: Optional[TransactionType] = Field(None, description="Transaction type")
    transaction_date: Optional[datetime] = Field(None, description="Transaction date")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    category_id: Optional[int] = Field(None, description="Category ID")


class TransactionResponse(BaseModel):
    """Transaction response schema"""
    id: int
    user_id: int
    amount: float
    type: TransactionType
    transaction_date: datetime  # Always present in response
    description: Optional[str]
    category_id: Optional[int]
    category: Optional[CategoryResponse] = None  # Nested category data
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


    