"""
TradeForge AaaS - Authentication API
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Authentication endpoints for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.core.i18n import t

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
    
    Returns:
        Created user data
    
    Raises:
        HTTPException: If user already exists
    """
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=t("user_already_exists")
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
        is_verified=False,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """
    User login.
    
    Args:
        login_data: Login credentials
        db: Database session
    
    Returns:
        Access and refresh tokens
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=t("invalid_credentials"),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_token: Refresh token
        db: Database session
    
    Returns:
        New access and refresh tokens
    """
    # TODO: Implement token refresh logic
    # Decode refresh token, verify, and create new tokens
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token endpoint not yet implemented"
    )


# Export router
__all__ = ["router"]
