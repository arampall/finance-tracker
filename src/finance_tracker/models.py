from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, Enum as SAEnum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum   
from typing import List, Optional
from .database import Base

__all__ = ["Base", "TransactionType", "User", "Category", "Transaction"]    

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uix_category_name_user"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="categories")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description})"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"), index=True, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[TransactionType] = mapped_column(SAEnum(TransactionType), nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, amount={self.amount}, description={self.description})"