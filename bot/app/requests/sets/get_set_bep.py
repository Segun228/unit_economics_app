import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import io
import zipfile


async def get_unit_bep(telegram_id, unit_id):
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    if not base_url or not telegram_id:
        raise ValueError("BASE_URL or telegram_id not provided")

    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {telegram_id}",
        }
        exact_url = f"{base_url}analitics/evaluate/unit/{unit_id}/break_even_point/"

        async with session.post(exact_url, headers=headers) as response:
            if response.status in (200, 201):
                image_bytes = await response.read()
                return [image_bytes]
            else:
                logging.error(f"Ошибка: {response.status}")
                return None