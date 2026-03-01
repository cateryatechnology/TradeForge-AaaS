"""
TradeForge AaaS - Database Models
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

SQLAlchemy models for database tables.
"""

from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class SubscriptionPlan(str, enum.Enum):
    """Subscription plan types."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    api_keys = relationship("ExchangeAPIKey", back_populates="user", cascade="all, delete-orphan")
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")


class ExchangeAPIKey(Base):
    """Exchange API keys (encrypted)."""
    __tablename__ = "exchange_api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exchange = Column(String(50), nullable=False)  # binance, bybit, etc.
    encrypted_api_key = Column(Text, nullable=False)
    encrypted_api_secret = Column(Text, nullable=False)
    is_testnet = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="api_keys")


class Wallet(Base):
    """Crypto wallet addresses."""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    network = Column(String(50), nullable=False)  # ethereum, polygon, arbitrum
    address = Column(String(255), nullable=False)
    encrypted_private_key = Column(Text)  # Optional, only if user wants to execute txs
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wallets")


class Strategy(Base):
    """Trading strategies."""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    strategy_type = Column(String(50))  # sma_crossover, rsi, custom, etc.
    parameters = Column(Text)  # JSON string of parameters
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="strategies")
    backtests = relationship("Backtest", back_populates="strategy", cascade="all, delete-orphan")


class Backtest(Base):
    """Backtest results."""
    __tablename__ = "backtests"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    final_capital = Column(Float, nullable=False)
    total_return = Column(Float)
    total_trades = Column(Integer)
    win_rate = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    results_json = Column(Text)  # Full results as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    strategy = relationship("Strategy", back_populates="backtests")


class Trade(Base):
    """Live trades."""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # BUY, SELL
    order_type = Column(String(20))  # MARKET, LIMIT
    quantity = Column(Float, nullable=False)
    price = Column(Float)
    executed_price = Column(Float)
    status = Column(String(20))  # PENDING, FILLED, CANCELLED
    order_id = Column(String(255))  # Exchange order ID
    pnl = Column(Float)
    commission = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="trades")


# Export all models
__all__ = [
    "User",
    "ExchangeAPIKey",
    "Wallet",
    "Strategy",
    "Backtest",
    "Trade",
    "SubscriptionPlan",
]
