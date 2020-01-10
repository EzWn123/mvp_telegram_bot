from dataclasses import dataclass, field
from typing import ClassVar
import datetime


@dataclass
class User():
    messenger_id: int
    id: int = None
    surname: str = None
    name: str = None
    second_name: str = None
    birthday: str = None
    age: int = 0
    sex: str = None
    nationality: str = None
    mobile_phone: str = None
    email: str = None
    passport_data: str = None
    military_card: str = None
    education: str = None
    state: int = 0

    _endpoint: ClassVar = 'users/'


@dataclass
class Message():
    user: int = None
    text: str = None
    id: int = None
    from_user: bool = False

    _endpoint: ClassVar = 'messages/'
