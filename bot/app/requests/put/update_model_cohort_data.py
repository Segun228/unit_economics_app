import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def update_model_cohort_data(
            telegram_id,
            set_id,
            model_id,
            retention,
            growth
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
        exact_url = f"{base_url}api/sets/{set_id}/units/{model_id}/" 
        logging.debug(f"Sending to {exact_url}")
        data = {
            "RR": retention/100,
            "AGR": growth/100
        }
        async with session.patch(
            exact_url, 
            headers=headers,
            json = data
        ) as response:
            if response.status in (200, 201, 202, 203):
                logging.info("обновлено")
                return await response.json()
            else:
                return None