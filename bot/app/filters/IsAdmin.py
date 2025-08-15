from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import load_dotenv
import logging
import os



load_dotenv()


def parse_admin_id(env_name: str):
    value = os.getenv(env_name, "").strip()
    if value.isdigit():
        return int(value)
    return None


ADMIN_IDS = list(filter(None, [
    parse_admin_id("ADMIN_1"),
    parse_admin_id("ADMIN_2"),
]))



class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        is_admin = user_id in ADMIN_IDS
        return is_admin