from src.Domain.PromptSales.Contracts.PaymentContracts import PaymentRequestDTO, PaymentResponseDTO
from src.Domain.PromptSales.Infrastructure.Repositories.PaymentRepository import IPaymentRepository  # Interface
# Import the PaymentStrategy as well (or define it here if it's small)
from src.Domain.PromptSales.Services.PaymentServices.PaymentStrategies import PaymentStrategy


class PaymentContextService:
    # We inject BOTH the Strategy (business logic) AND the Repository (persistence)
    def __init__(self, strategy: PaymentStrategy, repository: IPaymentRepository):
        self.strategy = strategy
        self.repository = repository

    async def execute(self, data: PaymentRequestDTO):
        # 1. Process payment using the selected strategy (PayPal/Stripe)
        result_message = await self.strategy.process_payment(data)
        
        # 2. Create the result DTO
        response_dto = PaymentResponseDTO(
            transaction_id="GEN-123",  # Real generated ID would come from the strategy
            status="completed",
            message=result_message
        )

        # 3. SAVE to the database using the REPOSITORY
        # The service does not write SQL; it simply tells the repo "save this".
        await self.repository.save(response_dto)

        return response_dto
