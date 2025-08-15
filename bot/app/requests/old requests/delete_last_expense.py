import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint

from app.requests.get_last_expense import get_last_expense

async def delete_last_expense(telegram_id):
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    if not base_url or base_url is None:
        logging.error("No base URL was provided")
        raise ValueError("No base URL was provided")
    if not telegram_id or telegram_id is None:
        logging.error("No base telegram_id was provided")
        raise ValueError("No telegram_id was provided")

    last_post = await get_last_expense(telegram_id=telegram_id)
    if not last_post:
        logging.warning("Нет записей для удаления.")
        return False
        
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {telegram_id}",
        }
        async with session.delete(
            base_url + f"api/expenses/{last_post.get('id')}/", 
            headers=headers,
        ) as response:
            if response.status in (200, 204):
                logging.info(f"Запись '{last_post.get('title')}' успешно удалена. Статус: {response.status}")
                return True
            else:
                logging.error(f"Ошибка при удалении: {response.status}")
                return False

async def main():
    response_data = await delete_last_expense(telegram_id="6911237041")
    if response_data:
        print("\n--- Запись успешно удалена ---")
    else:
        print("\n--- Не удалось удалить запись ---")

if __name__ == "__main__":
    asyncio.run(main())