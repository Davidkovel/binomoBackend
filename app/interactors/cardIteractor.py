from app.database.repositories.cardRepository import CardRepository
from app.schemas.user import BankCardResponse


class CardIteractor:
    def __init__(self, card_repository: CardRepository):
        self.card_repository = card_repository

    async def get_bank_card(self) -> BankCardResponse:
        card = await self.card_repository.get_card_number()

        if card is None:
            card = "8600 0000 0000 0000"  # дефолтное значение

        return BankCardResponse(card_number=card)

    async def set_bank_card(self, card_number: str, card_holder_name: str) -> BankCardResponse:
        card_number, card_holder_name = await self.card_repository.set_card_data(
            card_number=card_number,
            card_holder_name=card_holder_name
        )

        return BankCardResponse(card_number=card_number)
