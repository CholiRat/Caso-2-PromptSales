# Archivo: src/test/unit/test_crm_lead_processing.py
"""
Unit tests para procesamiento de leads en CRM
"""
import pytest
from unittest.mock import AsyncMock
from datetime import datetime
from src.Domain.PromptCRM.Services.ClientServices.LeadService import LeadService
from src.Domain.PromptCRM.Contracts.ClientContracts import LeadRegistrationRequest

class TestCRMLeadProcessing:
    """Pruebas unitarias para procesamiento de leads"""
    
    @pytest.fixture
    def lead_service(self):
        """Fixture para servicio de leads con dependencias mockeadas"""
        mock_repo = AsyncMock()
        mock_repo.save_lead = AsyncMock(return_value={"id": "lead_456", "score": 85})
        mock_repo.update_lead_score = AsyncMock(return_value=True)
        
        mock_ai_predictor = AsyncMock()
        mock_ai_predictor.predict_purchase_intent = AsyncMock(return_value=0.75)
        
        return LeadService(
            repository=mock_repo,
            ai_predictor=mock_ai_predictor,
            cache=AsyncMock()
        )
    
    @pytest.mark.asyncio
    async def test_lead_registration_and_scoring(self, lead_service):
        """Prueba registro de lead y cálculo de score"""
        lead_request = LeadRegistrationRequest(
            name="Juan Pérez",
            email="juan@example.com",
            phone="+1234567890",
            company="Tech Corp",
            source="website_form",
            interest_areas=["marketing automation", "AI tools"]
        )
        
        result = await lead_service.register_lead(lead_request)
        
        assert result["id"] == "lead_456"
        assert result["score"] == 85  # Score calculado
        assert lead_service.repository.save_lead.called
        assert lead_service.ai_predictor.predict_purchase_intent.called
    
    @pytest.mark.asyncio
    async def test_lead_scoring_accuracy(self, lead_service):
        """Valida que el scoring de leads sea consistente"""
        # Lead con alta probabilidad de compra
        high_value_lead = LeadRegistrationRequest(
            name="Maria García",
            email="maria@enterprise.com",
            company="Enterprise Inc",
            source="linkedin",
            interest_areas=["enterprise solution", "yearly contract"],
            budget=50000
        )
        
        result = await lead_service.register_lead(high_value_lead)
        
        # Lead de alta calidad debe tener score > 70
        assert result["score"] > 70, f"Score bajo para lead de alta calidad: {result['score']}"
    
    @pytest.mark.asyncio
    async def test_lead_processing_performance(self, lead_service):
        """Valida rendimiento en procesamiento de leads"""
        import time
        
        lead_request = LeadRegistrationRequest(
            name="Test Performance",
            email="test@example.com",
            source="api"
        )
        
        start_time = time.time()
        await lead_service.register_lead(lead_request)
        processing_time = time.time() - start_time
        
        # Procesamiento de lead debe ser rápido (< 1 segundo)
        assert processing_time < 1.0, f"Procesamiento lento: {processing_time:.2f}s"