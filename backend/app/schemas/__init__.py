"""
TradeForge AaaS - Pydantic Schemas
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================
# ENUMS
# ============================================

class SubscriptionPlan(str, Enum):
    """Subscription plan types."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class OrderSide(str, Enum):
    """Order side."""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"


class OrderStatus(str, Enum):
    """Order status."""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    FAILED = "failed"


# ============================================
# USER SCHEMAS
# ============================================

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_verified: bool
    subscription_plan: SubscriptionPlan
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating user."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None


# ============================================
# AUTH SCHEMAS
# ============================================

class Token(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: Optional[int] = None
    email: Optional[str] = None


# ============================================
# EXCHANGE API KEY SCHEMAS
# ============================================

class ExchangeAPIKeyCreate(BaseModel):
    """Schema for creating exchange API key."""
    exchange: str = Field(..., min_length=1, max_length=50)
    api_key: str = Field(..., min_length=1)
    api_secret: str = Field(..., min_length=1)
    is_testnet: bool = True


class ExchangeAPIKeyResponse(BaseModel):
    """Schema for exchange API key response."""
    id: int
    exchange: str
    is_testnet: bool
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# WALLET SCHEMAS
# ============================================

class WalletCreate(BaseModel):
    """Schema for creating wallet."""
    network: str = Field(..., min_length=1, max_length=50)
    address: str = Field(..., min_length=1, max_length=255)
    private_key: Optional[str] = None  # Encrypted before storage


class WalletResponse(BaseModel):
    """Schema for wallet response."""
    id: int
    network: str
    address: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# STRATEGY SCHEMAS
# ============================================

class StrategyCreate(BaseModel):
    """Schema for creating strategy."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    strategy_type: str
    parameters: Dict[str, Any] = {}


class StrategyResponse(BaseModel):
    """Schema for strategy response."""
    id: int
    name: str
    description: Optional[str]
    strategy_type: str
    parameters: Optional[str]
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# BACKTEST SCHEMAS
# ============================================

class BacktestRequest(BaseModel):
    """Schema for backtest request."""
    strategy_id: int
    symbol: str = Field(..., min_length=1, max_length=20)
    timeframe: str = Field(..., min_length=1, max_length=10)
    start_date: datetime
    end_date: datetime
    initial_capital: float = Field(default=10000.0, gt=0)
    commission: float = Field(default=0.001, ge=0, le=1)


class BacktestResponse(BaseModel):
    """Schema for backtest response."""
    id: int
    strategy_id: int
    symbol: str
    timeframe: str
    initial_capital: float
    final_capital: float
    total_return: Optional[float]
    total_trades: Optional[int]
    win_rate: Optional[float]
    sharpe_ratio: Optional[float]
    max_drawdown: Optional[float]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# TRADE SCHEMAS
# ============================================

class TradeCreate(BaseModel):
    """Schema for creating trade."""
    exchange: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float = Field(..., gt=0)
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class TradeResponse(BaseModel):
    """Schema for trade response."""
    id: int
    exchange: str
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]
    executed_price: Optional[float]
    status: str
    pnl: Optional[float]
    commission: Optional[float]
    created_at: datetime
    executed_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


# ============================================
# DEFI SCHEMAS
# ============================================

class SwapRequest(BaseModel):
    """Schema for token swap request."""
    network: str
    token_in: str
    token_out: str
    amount_in: float = Field(..., gt=0)
    slippage_tolerance: float = Field(default=0.5, ge=0.1, le=10)
    fee_tier: int = Field(default=3000)


class SwapResponse(BaseModel):
    """Schema for swap response."""
    transaction_hash: Optional[str]
    status: str
    amount_in: float
    amount_out: float
    token_in: str
    token_out: str


class LendRequest(BaseModel):
    """Schema for lending request (Aave)."""
    network: str
    asset: str
    amount: float = Field(..., gt=0)


class BorrowRequest(BaseModel):
    """Schema for borrow request (Aave)."""
    network: str
    asset: str
    amount: float = Field(..., gt=0)
    interest_rate_mode: int = Field(default=2, ge=1, le=2)  # 1=stable, 2=variable


# ============================================
# COMMON SCHEMAS
# ============================================

class Message(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    status_code: int


# Export all schemas
__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "Token",
    "TokenData",
    "ExchangeAPIKeyCreate",
    "ExchangeAPIKeyResponse",
    "WalletCreate",
    "WalletResponse",
    "StrategyCreate",
    "StrategyResponse",
    "BacktestRequest",
    "BacktestResponse",
    "TradeCreate",
    "TradeResponse",
    "SwapRequest",
    "SwapResponse",
    "LendRequest",
    "BorrowRequest",
    "Message",
    "ErrorResponse",
    "SubscriptionPlan",
    "OrderSide",
    "OrderType",
    "OrderStatus",
]
