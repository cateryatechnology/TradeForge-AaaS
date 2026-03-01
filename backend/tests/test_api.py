"""
TradeForge AaaS - API Tests
Author: Ary HH
Email: aryhharyanto@proton.me
GitHub: https://github.com/AryHHAry
© 2026

Tests for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["author"] == "Ary HH"


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_info(client: TestClient):
    """Test API info endpoint."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TradeForge AaaS"
    assert "features" in data
    assert len(data["features"]) > 0


# TODO: Add more tests
# - User registration
# - User login
# - Token refresh
# - Protected endpoints
# - DeFi operations
# - Backtesting
