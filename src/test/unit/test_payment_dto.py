"""
Unit tests para DTOs de Pagos - Validación de contratos
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.Domain.PromptSales.Contracts.PaymentContracts import (
    SubscriptionPlan,
    Invoice
)

class TestPaymentDTOs:
    """Pruebas unitarias para DTOs de pago"""
    
    def test_subscription_plan_valid(self):
        """Valida que se pueda crear un plan de suscripción válido"""
        plan = SubscriptionPlan(
            id="basic_monthly",
            name="Básico Mensual",
            price=99.99,
            currency="USD",
            features=["1000 leads/mes", "Soporte básico"],
            tier=1
        )
        
        assert plan.id == "basic_monthly"
        assert plan.price == 99.99
        assert len(plan.features) == 2
    
    def test_invoice_creation(self):
        """Valida creación de factura con datos completos"""
        invoice = Invoice(
            id="INV-2024-001",
            customer_id="CUST-123",
            amount=299.99,
            currency="USD",
            status="paid",
            due_date=datetime.now(),
            created_at=datetime.now()
        )
        
        assert invoice.status == "paid"
        assert invoice.amount > 0
        assert invoice.id.startswith("INV-")
    
    def test_invoice_negative_amount_fails(self):
        """Valida que no se acepten montos negativos"""
        with pytest.raises(ValidationError):
            Invoice(
                id="INV-001",
                customer_id="CUST-123",
                amount=-100.00,  # Monto negativo debe fallar
                currency="USD",
                status="pending",
                due_date=datetime.now()
            )