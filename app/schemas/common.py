import re
from datetime import date
from typing import Annotated, List, Union

from pydantic import UUID4, EmailStr, Field, HttpUrl, conint, constr

Email = Annotated[
    EmailStr,
    Field(
        min_length=8,
        max_length=120,
        description="Email пользователя",
        examples=["cu_fan@edu.hse.ru"],
    ),
]

Password = Annotated[
    constr(
        min_length=8,
        max_length=60,
        pattern=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"),
    ),
    Field(
        min_length=8,
        max_length=60,
        description="Пароль пользователя/компании. Должен содержать латинские буквы, хотя бы одну заглавную, одну строчную, одну цифру и специальные символы.",
        examples=["HardPa$$w0rd!iamthewinner"],
    ),
]

UserId = Annotated[
    UUID4,
    Field(
        description="Уникальный идентификатор пользователя.",
        examples=["b5d53d5d-e866-44ee-8546-cf01d2e73152"],
    ),
]

UserFirstName = Annotated[
    constr(min_length=1, max_length=100),
    Field(
        min_length=1,
        max_length=100,
        description="Имя пользователя",
        examples=["Мария"],
    ),
]

Country = Annotated[
    constr(min_length=2, max_length=2),
    Field(
        min_length=2,
        max_length=2,
        description="Страна пользователя в формате ISO 3166-1 alpha-2, регистр может быть разным. Страна с данным кодом должна обязательно существовать.",
        examples=["ru"],
    ),
]
