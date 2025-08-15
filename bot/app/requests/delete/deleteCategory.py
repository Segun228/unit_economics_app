import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def delete_category(telegram_id, category_id):
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
        exact_url = f"{base_url}api/categories/{category_id}/" 
        logging.debug(f"Sending to {exact_url}")
        async with session.delete(
            exact_url, 
            headers=headers,
        ) as response:
            if response.status in (200, 201, 202, 203, 204):
                logging.info("категория удалена")
                return True
            else:
                return None


async def main():
    try:
        response_data = await delete_category(telegram_id=6911237041, category_id=4)
        pprint(response_data)
    except ValueError:
        print("Пожалуйста, введите корректный числовой ID.")


if __name__ == "__main__":
    asyncio.run(main())