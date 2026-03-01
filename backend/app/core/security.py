"""
TradeForge AaaS - Security Module
Author: Ary HH
Email: cateryatechnology@proton.me
GitHub: https://github.com/cateryatechnology
© 2026

Security utilities for authentication, password hashing, and encryption.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import base64
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
    
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Data to encode in token
    
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token to decode
    
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


class EncryptionService:
    """
    Service for encrypting/decrypting sensitive data like API keys and private keys.
    Uses Fernet (symmetric encryption) from cryptography library.
    """
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption service.
        
        Args:
            encryption_key: Base64 encoded encryption key.
                           If not provided, uses key from settings.
        """
        key = encryption_key or settings.ENCRYPTION_KEY
        
        if not key:
            # Generate a new key if none provided (development only)
            key = Fernet.generate_key().decode()
            print(f"⚠️  WARNING: Generated new encryption key: {key}")
            print("⚠️  Add this to your .env file as ENCRYPTION_KEY")
        
        # Ensure key is bytes
        if isinstance(key, str):
            key = key.encode()
        
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data.
        
        Args:
            data: Plain text data to encrypt
        
        Returns:
            Base64 encoded encrypted data
        """
        if not data:
            return ""
        
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Base64 encoded encrypted data
        
        Returns:
            Decrypted plain text data
        """
        if not encrypted_data:
            return ""
        
        try:
            decoded = base64.b64decode(encrypted_data.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new encryption key.
        
        Returns:
            Base64 encoded encryption key
        """
        return Fernet.generate_key().decode()


# Singleton encryption service
encryption_service = EncryptionService()


def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt an API key for storage.
    
    Args:
        api_key: Plain text API key
    
    Returns:
        Encrypted API key
    """
    return encryption_service.encrypt(api_key)


def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt an API key from storage.
    
    Args:
        encrypted_key: Encrypted API key
    
    Returns:
        Plain text API key
    """
    return encryption_service.decrypt(encrypted_key)


def encrypt_private_key(private_key: str) -> str:
    """
    Encrypt a wallet private key for storage.
    
    Args:
        private_key: Plain text private key
    
    Returns:
        Encrypted private key
    """
    return encryption_service.encrypt(private_key)


def decrypt_private_key(encrypted_key: str) -> str:
    """
    Decrypt a wallet private key from storage.
    
    Args:
        encrypted_key: Encrypted private key
    
    Returns:
        Plain text private key
    """
    return encryption_service.decrypt(encrypted_key)


# Export for convenience
__all__ = [
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "EncryptionService",
    "encryption_service",
    "encrypt_api_key",
    "decrypt_api_key",
    "encrypt_private_key",
    "decrypt_private_key",
]
