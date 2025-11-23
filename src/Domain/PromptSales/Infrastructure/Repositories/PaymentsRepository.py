from abc import ABC, abstractmethod
from typing import Optional
from src.Domain.PromptSales.Contracts.PaymentContracts import PaymentResponseDTO
# We assume a DB model called PaymentModel
# from src.Database.Models import PaymentModel 

# 1. The Interface (Repository Contract)
# This defines WHAT can be done, but not HOW.
class IPaymentRepository(ABC):
    @abstractmethod
    async def save(self, payment: PaymentResponseDTO) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: str) -> Optional[PaymentResponseDTO]:
        pass

# 2. The Concrete Implementation (SQL Server with SQLAlchemy)
# This defines HOW it is done (SQL, commits, etc.)
class SqlPaymentRepository(IPaymentRepository):
    def __init__(self, db_session):
        self.db = db_session

    async def save(self, payment_dto: PaymentResponseDTO) -> bool:
        try:
            # Convert DTO to Database Model (Mapping)
            new_record = PaymentModel(
                trans_id=payment_dto.transaction_id,
                amount=payment_dto.amount,
                status=payment_dto.status
            )
            self.db.add(new_record)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            return False

    async def get_by_id(self, transaction_id: str) -> Optional[PaymentResponseDTO]:
        # Logic to query SQL
        record = await self.db.query(PaymentModel).filter_by(trans_id=transaction_id).first()
        if record:
            return PaymentResponseDTO(**record.__dict__)
        return None