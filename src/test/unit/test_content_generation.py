"""
Unit tests para generación de contenido - IA y validaciones
"""
import pytest
from unittest.mock import patch, AsyncMock
from src.Domain.PromptContent.Services.GeneratedContentServices.ContentGenerationService import (
    ContentGenerationService
)
from src.Domain.PromptContent.Contracts.GeneratedContentContracts import ContentRequest

class TestContentGeneration:
    """Pruebas unitarias para generación de contenido"""
    
    @pytest.fixture
    def content_service(self):
        """Fixture para servicio de contenido"""
        mock_ai_provider = AsyncMock()
        mock_ai_provider.generate_text = AsyncMock(
            return_value="Texto generado por IA para campaña de marketing"
        )
        mock_ai_provider.generate_image = AsyncMock(
            return_value="https://cdn.promptsales.com/generated/image_123.png"
        )
        
        return ContentGenerationService(
            ai_provider=mock_ai_provider,
            cache_client=AsyncMock()
        )
    
    @pytest.mark.asyncio
    async def test_text_generation_with_prompt(self, content_service):
        """Prueba generación de texto con prompt específico"""
        request = ContentRequest(
            prompt="Crea un anuncio para nuevo smartphone",
            content_type="text",
            tone="profesional",
            target_language="es"
        )
        
        result = await content_service.generate_text_content(request)
        
        assert result is not None
        assert "IA" in result  # Verifica que fue generado por IA
        assert content_service.ai_provider.generate_text.called
    
    @pytest.mark.asyncio
    async def test_content_generation_performance(self, content_service):
        """Valida que la generación de contenido respete límites de tiempo"""
        import time
        
        request = ContentRequest(
            prompt="Genera contenido extenso para blog",
            content_type="text",
            tone="informal",
            word_count=500
        )
        
        start_time = time.time()
        result = await content_service.generate_text_content(request)
        execution_time = time.time() - start_time
        
        # Valida requerimiento: < 20 segundos para operaciones complejas
        assert execution_time < 20.0, f"Generación tomó {execution_time:.2f}s"
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_multimedia_content_generation(self, content_service):
        """Prueba generación de contenido multimedia"""
        request = ContentRequest(
            prompt="Imagen para campaña de verano",
            content_type="image",
            style="modern",
            dimensions={"width": 1200, "height": 800}
        )
        
        result = await content_service.generate_image_content(request)
        
        assert "https://" in result  # Debe devolver URL
        assert content_service.ai_provider.generate_image.called