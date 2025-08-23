import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import io
import zipfile

from io import BytesIO


async def get_unit_exel( 
        telegram_id, 
        unit_id
    ):
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    if not base_url:
        logging.error("No base URL was provided")
        raise ValueError("No base URL was provided")
    if not telegram_id:
        logging.error("No base telegram_id was provided")
        raise ValueError("No telegram_id was provided")
        
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {telegram_id}",
        }
        exact_url = f"{base_url}analitics/report/unit/{unit_id}/xlsx/" 
        logging.debug(f"Sending to {exact_url}")
        async with session.post(
            exact_url, 
            headers=headers,
        ) as response:
            if response.status in (200, 201, 202, 203):
                logging.info("Report received")
                data = await response.read()
                file_like = BytesIO(data)
                file_like.name = "report.xlsx" 
                return file_like
            else:
                return None