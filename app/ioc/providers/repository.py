from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine

from app.database.postgres.session import get_db
from app.database.repositories.cardRepository import CardRepository
from app.database.repositories.moneyRepository import MoneyRepository
from app.database.repositories.user import UserRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_user_repository(self, engine: AsyncEngine) -> AsyncIterable[UserRepository]:
        async for db_session in get_db(engine):
            yield UserRepository(db_session)

    @provide
    async def get_money_repository(self, engine: AsyncEngine) -> AsyncIterable[MoneyRepository]:
        async for db_session in get_db(engine):
            yield MoneyRepository(db_session)

    @provide
    async def get_card_repository(self, engine: AsyncEngine) -> AsyncIterable[CardRepository]:
        async for db_session in get_db(engine):
            yield CardRepository(db_session)
