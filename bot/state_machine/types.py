from dataclasses import dataclass
from typing import Dict


class Bot():
    def send_message(self, user_id, text, buttons=None, buttons_rows=2, parse_mode='Html'):
        pass


@dataclass
class Event():
    user: Dict[str, str]
    data: str
    event_type: str
    message_id: str = None


@dataclass
class InlineButton():
    text: str
    callback: str


@dataclass
class KeyboardButton():
    text: str
