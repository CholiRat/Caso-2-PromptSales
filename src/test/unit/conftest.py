"""
Configuración global para pruebas unitarias
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

# Fixtures globales
@pytest.fixture
def mock_redis():
    """Fixture global para Redis mockeado"""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    return redis

@pytest.fixture
def mock_db_session():
    """Fixture global para sesión de BD mockeada"""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.execute = AsyncMock()
    return session

@pytest.fixture
def sample_campaign_data():
    """Datos de ejemplo para campañas"""
    return {
        "id": "campaign_001",
        "name": "Test Campaign",
        "budget": 10000.00,
        "status": "active",
        "metrics": {
            "impressions": 50000,
            "clicks": 2500,
            "conversions": 125
        }
    }

# Configuración de pytest
def pytest_configure(config):
    """Configuración global de pytest"""
    config.addinivalue_line(
        "markers",
        "performance: tests de rendimiento"
    )
    config.addinivalue_line(
        "markers", 
        "integration: tests de integración"
    )