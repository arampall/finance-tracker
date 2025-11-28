from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from ..models import User
from ..schemas import UserCreate, UserResponse, UserLogin
from ..database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Initialize CryptContext globally to avoid overhead on every request
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if user already exists
    user_query = select(User).where(User.email == user_data.email)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)

    # Create the user
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        username=user_data.username
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Login a user.
    """
    # Check if user exists
    user_query = select(User).where(User.email == user_data.email)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    # Exception if user credentials are incorrect
    invalid_credentials_exception = HTTPException(
        status_code=400, 
        detail="Incorrect email or password"
    )

    if not user:
        raise invalid_credentials_exception

    # Verify the password
    if not pwd_context.verify(user_data.password, user.password):
        raise invalid_credentials_exception

    return user

