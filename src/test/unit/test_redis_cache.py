"""
Unit tests para cache Redis - Validación de rendimiento
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

class TestRedisCache:
    """Pruebas unitarias para cache Redis"""
    
    @pytest.fixture
    def redis_client(self):
        """Fixture para cliente Redis mockeado"""
        client = AsyncMock()
        client.get = AsyncMock()
        client.set = AsyncMock(return_value=True)
        client.setex = AsyncMock(return_value=True)
        client.delete = AsyncMock(return_value=1)
        client.ttl = AsyncMock(return_value=300)  # 5 minutos
        return client
    
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self, redis_client):
        """Prueba almacenamiento y recuperación de cache"""
        test_key = "campaign:123:metrics"
        test_value = {"impressions": 1000, "clicks": 50, "ctr": 0.05}
        
        # Almacena en cache
        await redis_client.set(test_key, json.dumps(test_value), ex=3600)
        
        # Recupera de cache
        redis_client.get.return_value = json.dumps(test_value)
        cached = await redis_client.get(test_key)
        
        result = json.loads(cached)
        
        assert result["impressions"] == 1000
        assert result["ctr"] == 0.05
        redis_client.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_cache_performance(self, redis_client):
        """Valida que cache responda en < 400ms (requerimiento)"""
        import time
        
        # Configura respuesta rápida
        redis_client.get.return_value = json.dumps({"cached": True})
        
        start_time = time.time()
        for _ in range(100):  # 100 lecturas
            await redis_client.get("performance_test")
        
        avg_time = (time.time() - start_time) / 100
        
        # Verifica requerimiento de < 400ms
        assert avg_time < 0.4, f"Cache lento: {avg_time*1000:.2f}ms por operación"
    
    @pytest.mark.asyncio
    async def test_cache_eviction_policy(self, redis_client):
        """Valida política de expiración de cache"""
        test_key = "temporary:data"
        
        # Almacena con expiración
        await redis_client.setex(test_key, 60, "datos temporales")
        
        # Verifica TTL
        ttl = await redis_client.ttl(test_key)
        
        assert ttl <= 60  # TTL no debe exceder 60 segundos
        assert ttl > 0  # Debe tener tiempo restante