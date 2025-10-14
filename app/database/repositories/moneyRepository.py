from decimal import Decimal

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.exceptions import (
    InsufficientFundsError,
)

from app.database.postgres.models import (
    UserModel,
)
from app.schemas.common import UserId


class MoneyRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_balance(self, user_id: UserId) -> Decimal:
        """Получить баланс пользователя"""
        query = select(UserModel.balance).where(UserModel.id == user_id)
        result = await self.db_session.execute(query)
        balance = result.scalar_one_or_none()

        if balance is None:
            return Decimal('0.00')
        return balance

    async def deposit_money(self, user_id: UserId, amount: Decimal) -> Decimal:
        """Пополнить баланс"""
        # Получаем текущий баланс
        current_balance = await self.get_balance(user_id)
        new_balance = current_balance + amount

        # Обновляем баланс в базе
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(balance=new_balance)
            .execution_options(synchronize_session="fetch")
        )

        await self.db_session.execute(query)
        await self.db_session.commit()

        return new_balance

    async def withdraw_money(self, user_id: UserId, amount: Decimal) -> Decimal:
        """Снять деньги (для выводов или торговли)"""
        current_balance = await self.get_balance(user_id)
        print("current_balance", current_balance)
        # Проверяем достаточно ли средств
        if current_balance < amount:
            raise InsufficientFundsError

        print(f'calculating: Amount: {amount}, current_balance: {current_balance}')
        new_balance = current_balance - amount
        print('new_balance', new_balance)

        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(balance=new_balance)
            .execution_options(synchronize_session="fetch")
        )

        await self.db_session.execute(query)
        await self.db_session.commit()

        return new_balance

    async def set_balance(self, user_id: UserId, new_balance: Decimal) -> Decimal:
        """Установить конкретный баланс (админ функция)"""
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(balance=new_balance)
            .execution_options(synchronize_session="fetch")
        )

        await self.db_session.execute(query)
        await self.db_session.commit()

        return new_balance

    async def update_balance(self, user_id: UserId, amount_change: Decimal) -> Decimal:
        """Обновить баланс (прибавить/вычесть сумму)"""
        current_balance = await self.get_balance(user_id)
        new_balance = current_balance + amount_change

        if new_balance < 0:
            raise InsufficientFundsError("Insufficient funds")

        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(balance=new_balance)
            .execution_options(synchronize_session="fetch")
        )

        await self.db_session.execute(query)
        await self.db_session.commit()

        return new_balance