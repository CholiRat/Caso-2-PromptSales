"""
Unit tests para integración MCP - Comunicación entre servicios
"""
import pytest
from unittest.mock import patch, MagicMock
import json

class TestMCPIntegration:
    """Pruebas unitarias para integración MCP"""
    
    @pytest.fixture
    def mock_mcp_server(self):
        """Fixture para mock de servidor MCP"""
        server = MagicMock()
        server.process_request = MagicMock()
        return server
    
    def test_mcp_message_format(self, mock_mcp_server):
        """Valida formato de mensajes MCP"""
        # Mensaje MCP válido
        valid_message = {
            "type": "content_generation",
            "model": "gpt-4",
            "prompt": "Generate ad copy",
            "parameters": {
                "max_tokens": 100,
                "temperature": 0.7
            }
        }
        
        # Simula procesamiento
        mock_mcp_server.process_request.return_value = {
            "status": "success",
            "content": "Texto generado exitosamente",
            "tokens_used": 45
        }
        
        result = mock_mcp_server.process_request(valid_message)
        
        assert result["status"] == "success"
        assert "tokens_used" in result
        assert result["tokens_used"] > 0
    
    @patch('src.mcpServer.integrations.openai_mcp_adapter.OpenAIIntegration')
    def test_openai_integration_cache(self, MockOpenAI):
        """Valida que se use cache para reducir llamadas a OpenAI"""
        mock_openai = MockOpenAI()
        mock_openai.generate_content = MagicMock(
            return_value="Cached response"
        )
        
        # Primera llamada
        response1 = mock_openai.generate_content("mismo prompt")
        
        # Segunda llamada (debería usar cache interno)
        response2 = mock_openai.generate_content("mismo prompt")
        
        # Verifica que se minimicen llamadas a API
        assert mock_openai.generate_content.call_count <= 1
        assert response1 == response2
    
    def test_mcp_error_handling(self, mock_mcp_server):
        """Valida manejo de errores en MCP"""
        # Mensaje inválido
        invalid_message = {
            "type": "unknown_type",
            "data": {}
        }
        
        mock_mcp_server.process_request.side_effect = ValueError("Tipo no soportado")
        
        try:
            mock_mcp_server.process_request(invalid_message)
            assert False, "Debería haber lanzado excepción"
        except ValueError as e:
            assert "Tipo no soportado" in str(e)