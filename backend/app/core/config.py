"""
TradeForge AaaS - Configuration Module
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Application configuration using Pydantic Settings for type-safe environment variable loading.
"""

from typing import List, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All settings are type-safe and validated using Pydantic.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ============================================
    # APPLICATION
    # ============================================
    APP_NAME: str = "TradeForge AaaS"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # ============================================
    # DATABASE
    # ============================================
    POSTGRES_USER: str = "tradeforge"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "tradeforge_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # ============================================
    # REDIS
    # ============================================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL from components."""
        password_part = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{password_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # ============================================
    # SECURITY & AUTH
    # ============================================
    SECRET_KEY: str = "your_super_secret_key_change_this_in_production_min_32_chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENCRYPTION_KEY: str = ""  # Base64 encoded 32-byte key for encrypting API keys
    
    # ============================================
    # CORS
    # ============================================
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:8501",
        "http://localhost:3000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # ============================================
    # BLOCKCHAIN & WEB3
    # ============================================
    ETH_RPC_URL: str = "https://eth-mainnet.g.alchemy.com/v2/demo"
    ETH_CHAIN_ID: int = 1
    
    POLYGON_RPC_URL: str = "https://polygon-mainnet.g.alchemy.com/v2/demo"
    POLYGON_CHAIN_ID: int = 137
    
    ARBITRUM_RPC_URL: str = "https://arb-mainnet.g.alchemy.com/v2/demo"
    ARBITRUM_CHAIN_ID: int = 42161
    
    DEFAULT_NETWORK: str = "ethereum"
    
    # ============================================
    # DEFI PROTOCOLS
    # ============================================
    # Uniswap V3 (Ethereum Mainnet)
    UNISWAP_V3_ROUTER: str = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
    UNISWAP_V3_FACTORY: str = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
    
    # Aave V3 (Ethereum Mainnet)
    AAVE_V3_POOL: str = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
    AAVE_V3_POOL_DATA_PROVIDER: str = "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3"
    
    # Chainlink Price Feeds (Ethereum Mainnet)
    CHAINLINK_ETH_USD: str = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
    CHAINLINK_BTC_USD: str = "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"
    
    # ============================================
    # EXCHANGES
    # ============================================
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    BINANCE_TESTNET: bool = True
    
    BYBIT_API_KEY: str = ""
    BYBIT_API_SECRET: str = ""
    BYBIT_TESTNET: bool = True
    
    COINBASE_API_KEY: str = ""
    COINBASE_API_SECRET: str = ""
    
    KRAKEN_API_KEY: str = ""
    KRAKEN_API_SECRET: str = ""
    
    ALPACA_API_KEY: str = ""
    ALPACA_API_SECRET: str = ""
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    
    # ============================================
    # NOTIFICATIONS
    # ============================================
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    TELEGRAM_ENABLED: bool = False
    
    DISCORD_WEBHOOK_URL: str = ""
    DISCORD_ENABLED: bool = False
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@tradeforge.com"
    EMAIL_ENABLED: bool = False
    
    # ============================================
    # RISK MANAGEMENT
    # ============================================
    MAX_POSITION_SIZE_PERCENT: float = 5.0
    MAX_DAILY_LOSS_PERCENT: float = 2.0
    MAX_OPEN_POSITIONS: int = 10
    DEFAULT_STOP_LOSS_PERCENT: float = 2.0
    DEFAULT_TAKE_PROFIT_PERCENT: float = 5.0
    
    # ============================================
    # BACKTESTING
    # ============================================
    BACKTEST_DEFAULT_CAPITAL: float = 10000.0
    BACKTEST_DEFAULT_COMMISSION: float = 0.001
    BACKTEST_MAX_YEARS: int = 5
    
    # ============================================
    # SUBSCRIPTION & PAYMENT
    # ============================================
    STRIPE_PUBLIC_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # ============================================
    # RATE LIMITING
    # ============================================
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # ============================================
    # LOGGING
    # ============================================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE_PATH: str = "./logs/tradeforge.log"
    
    # ============================================
    # CELERY
    # ============================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # ============================================
    # FRONTEND
    # ============================================
    STREAMLIT_SERVER_PORT: int = 8501
    STREAMLIT_SERVER_ADDRESS: str = "0.0.0.0"
    STREAMLIT_SERVER_HEADLESS: bool = True
    DEFAULT_LANGUAGE: str = "en"
    
    class Config:
        """Pydantic config."""
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to avoid re-reading .env file on every call.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Singleton settings instance
settings = get_settings()


# Export for convenience
__all__ = ["settings", "get_settings", "Settings"]
