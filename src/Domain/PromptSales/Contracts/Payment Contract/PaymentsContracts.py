from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# DTO for request
class PaymentRequestDTO(BaseModel):
    user_id: str = Field(..., description="ID of the paying user")
    amount: float = Field(..., gt=0, description="Payment amount")
    currency: str = Field(default="USD", max_length=3)
    payment_method: str = Field(..., pattern="^(card|paypal|transfer)$")

# DTO for response
class PaymentResponseDTO(BaseModel):
    transaction_id: str
    status: str
    processed_at: datetime
    message: str