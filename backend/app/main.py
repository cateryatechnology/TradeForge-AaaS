"""
TradeForge AaaS - Main FastAPI Application
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Main application entry point with API routes and middleware configuration.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.i18n import t, Language
# from app.api.v1 import auth, backtest, trading, defi, users
# from app.database import engine, Base

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting TradeForge AaaS...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # TODO: Initialize database connection pool
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    
    # TODO: Initialize Redis connection
    # TODO: Start background tasks (if any)
    
    logger.info("✅ Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("🔴 Shutting down TradeForge AaaS...")
    
    # TODO: Close database connections
    # TODO: Close Redis connections
    # TODO: Cleanup background tasks
    
    logger.info("✅ Application shut down successfully")


# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Algorithm-as-a-Service Trading Platform with DeFi Integration\n\n"
        "**Author:** Ary HH\n\n"
        "**Email:** cateryatechnology@proton.me\n\n"
        "**GitHub:** https://github.com/cateryatechnology\n\n"
        "© 2026"
    ),
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)


# ============================================
# MIDDLEWARE
# ============================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to all responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ============================================
# EXCEPTION HANDLERS
# ============================================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error" if not settings.DEBUG else str(exc),
        },
    )


# ============================================
# ROOT ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to TradeForge AaaS",
        "version": settings.APP_VERSION,
        "author": "Ary HH",
        "email": "cateryatechnology@proton.me",
        "github": "https://github.com/cateryatechnology",
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }


@app.get("/api/v1/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "author": "Ary HH",
        "email": "cateryatechnology@proton.me",
        "github": "https://github.com/cateryatechnology",
        "supported_languages": ["en", "id"],
        "features": [
            "Multi-tenant authentication",
            "Backtesting engine",
            "Live trading (CEX via CCXT)",
            "DeFi operations (Uniswap V3, Aave V3)",
            "Risk management",
            "Bilingual support (EN/ID)",
        ],
    }


# ============================================
# API ROUTES
# ============================================

# TODO: Include API routers when implemented
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(backtest.router, prefix="/api/v1/backtest", tags=["Backtesting"])
# app.include_router(trading.router, prefix="/api/v1/trading", tags=["Trading"])
# app.include_router(defi.router, prefix="/api/v1/defi", tags=["DeFi"])


# ============================================
# EXAMPLE ENDPOINTS (MVP)
# ============================================

@app.get("/api/v1/test/translate")
async def test_translation(key: str, language: str = "en"):
    """
    Test translation endpoint.
    
    Args:
        key: Translation key
        language: Language code (en or id)
    
    Returns:
        Translated message
    """
    try:
        lang = Language(language)
        translated = t(key, lang)
        return {
            "key": key,
            "language": language,
            "translation": translated,
        }
    except ValueError:
        return {
            "error": "Invalid language code. Use 'en' or 'id'.",
        }


@app.get("/api/v1/test/defi-price")
async def test_defi_price():
    """
    Test DeFi price feed endpoint.
    Get ETH and BTC prices from Chainlink.
    """
    try:
        from app.services.defi_service import DeFiService
        
        defi_service = DeFiService()
        
        eth_price = defi_service.get_eth_usd_price()
        btc_price = defi_service.get_btc_usd_price()
        
        return {
            "eth_usd": float(eth_price),
            "btc_usd": float(btc_price),
            "source": "Chainlink Price Feeds",
            "network": settings.DEFAULT_NETWORK,
        }
    except Exception as e:
        logger.error(f"Failed to fetch prices: {str(e)}")
        return {
            "error": "Failed to fetch prices",
            "detail": str(e) if settings.DEBUG else "Internal error",
        }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
