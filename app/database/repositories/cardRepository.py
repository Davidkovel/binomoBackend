from dns.e164 import query
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.postgres.models import BankCardModel


class CardRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_card_number(self) -> str:
        query = select(BankCardModel.card_number)
        result = await self.db_session.execute(query)
        card_number = result.scalar_one_or_none()

        # Если карты нет в базе, возвращаем дефолтное значение
        if card_number is None:
            return "8600 0000 0000 0000"  # или любое другое дефолтное значение

        return card_number

    async def set_card_number(self, card_number: str) -> str:
        # Сначала проверяем, есть ли уже запись
        existing_query = select(BankCardModel)
        existing_result = await self.db_session.execute(existing_query)
        existing_card = existing_result.scalar_one_or_none()

        if existing_card:
            # Обновляем существующую запись
            query = (
                update(BankCardModel)
                .where(BankCardModel.id == existing_card.id)
                .values(card_number=card_number)
            )
        else:
            # Создаем новую запись
            new_card = BankCardModel(card_number=card_number)
            self.db_session.add(new_card)

        await self.db_session.commit()
        return card_number
