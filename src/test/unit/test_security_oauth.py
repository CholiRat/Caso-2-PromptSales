"""
Unit tests para seguridad OAuth 2.0
"""
import pytest
from unittest.mock import patch, MagicMock
import jwt
from datetime import datetime, timedelta

class TestOAuthSecurity:
    """Pruebas unitarias para seguridad OAuth"""
    
    def test_jwt_token_validation(self):
        """Valida creación y verificación de tokens JWT"""
        secret_key = "test_secret_key"
        payload = {
            "sub": "user_123",
            "email": "user@promptsales.com",
            "role": "marketing_manager",
            "exp": datetime.now() + timedelta(hours=1)
        }
        
        # Genera token
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        # Decodifica y verifica
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        assert decoded["sub"] == "user_123"
        assert decoded["role"] == "marketing_manager"
        assert "exp" in decoded
    
    def test_token_expiration(self):
        """Valida que tokens expirados sean rechazados"""
        secret_key = "test_secret"
        
        # Token expirado hace 1 hora
        expired_payload = {
            "sub": "user_123",
            "exp": datetime.now() - timedelta(hours=1)
        }
        
        token = jwt.encode(expired_payload, secret_key, algorithm="HS256")
        
        try:
            jwt.decode(token, secret_key, algorithms=["HS256"])
            assert False, "Debería haber fallado por token expirado"
        except jwt.ExpiredSignatureError:
            assert True  # Esperado
    
    def test_role_based_access(self):
        """Valida control de acceso basado en roles"""
        # Token con rol de usuario básico
        user_token = {
            "sub": "basic_user",
            "role": "user",
            "permissions": ["read_campaigns", "create_content"]
        }
        
        # Token con rol de administrador
        admin_token = {
            "sub": "admin_user",
            "role": "admin",
            "permissions": ["read_all", "write_all", "delete", "approve"]
        }
        
        # Simula verificación de permisos
        def has_permission(token, required_permission):
            return required_permission in token["permissions"]
        
        # Usuario básico NO debería poder aprobar campañas
        assert not has_permission(user_token, "approve")
        
        # Administrador SÍ debería poder
        assert has_permission(admin_token, "approve")
        assert has_permission(admin_token, "delete")