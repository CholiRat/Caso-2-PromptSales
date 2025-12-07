"""
Unit tests para servicios de campañas - Lógica de negocio
"""
import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime, timedelta
from src.Domain.PromptAds.Services.CampaignServices.CampaignService import CampaignService
from src.Domain.PromptAds.Contracts.CampaignContracts import CreateCampaignRequest

class TestCampaignService:
    """Pruebas unitarias para servicios de campaña"""
    
    @pytest.fixture
    def mock_repository(self):
        """Fixture para mock del repositorio"""
        repo = Mock()
        repo.save = AsyncMock(return_value={"id": "campaign_123", "status": "draft"})
        repo.find_by_id = AsyncMock(return_value=None)
        return repo
    
    @pytest.fixture
    def mock_cache(self):
        """Fixture para mock de Redis cache"""
        cache = Mock()
        cache.get = AsyncMock(return_value=None)
        cache.set = AsyncMock(return_value=True)
        return cache
    
    @pytest.fixture
    def campaign_service(self, mock_repository, mock_cache):
        """Fixture para el servicio con dependencias mockeadas"""
        return CampaignService(mock_repository, mock_cache)
    
    @pytest.mark.asyncio
    async def test_create_campaign_with_valid_budget(self, campaign_service):
        """Prueba creación de campaña con presupuesto válido"""
        request = CreateCampaignRequest(
            name="Campaña Black Friday",
            budget=5000.00,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            target_audience="mujeres_25_40",
            channels=["facebook", "instagram"]
        )
        
        result = await campaign_service.create_campaign(request)
        
        assert result["id"] is not None
        assert result["status"] == "draft"
        assert campaign_service.repository.save.called
    
    @pytest.mark.asyncio
    async def test_campaign_optimization_performance(self, campaign_service):
        """Valida que la optimización se complete en menos de 7 segundos"""
        import time
        
        start_time = time.time()
        await campaign_service.optimize_campaign("campaign_123")
        execution_time = time.time() - start_time
        
        # Valida requerimiento de rendimiento: < 7 segundos
        assert execution_time < 7.0, f"Optimización tomó {execution_time:.2f}s, máximo 7s"
    
    @pytest.mark.asyncio
    async def test_campaign_uses_cache(self, campaign_service, mock_cache):
        """Valida que se use cache para campañas frecuentes"""
        campaign_id = "frequent_campaign_123"
        
        # Primera llamada - no en cache
        mock_cache.get.return_value = None
        await campaign_service.get_campaign(campaign_id)
        assert mock_cache.get.called
        
        # Segunda llamada - debería usar cache
        mock_cache.get.return_value = {"id": campaign_id, "cached": True}
        result = await campaign_service.get_campaign(campaign_id)
        
        # Verifica que se haya usado cache
        assert result.get("cached") is True
        assert campaign_service.repository.find_by_id.call_count <= 1  # Solo llamado una vez