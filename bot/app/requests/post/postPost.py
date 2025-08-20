import aiohttp
import asyncio
import os
import logging
from dotenv import load_dotenv
from pprint import pprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def post_post( 
        telegram_id, 
        category_id, 
        name,
        users,
        customers,
        AVP,
        APC,
        TMS,
        COGS,
        COGS1s,
        FC
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
        exact_url = f"{base_url}api/sets/{category_id}/units/" 
        logging.debug(f"Sending to {exact_url}")
        data = {
            "users": users,
            "customers":customers,
            "AVP":AVP,
            "APC":APC,
            "TMS":TMS,
            "COGS":COGS,
            "COGS1s":COGS1s,
            "FC":FC,
            "name":name,
        }
        print(data)
        async with session.post(
            exact_url, 
            headers=headers,
            data = data
        ) as response:
            if response.status in (200, 201, 202, 203):
                logging.info("категории получены")
                return await response.json()
            else:
                return None


async def main():
    try:
        response_data = await post_post( 
            telegram_id = 777, 
            category_id=1,
            name= "new",
            users = 1000,
            customers = 10,
            AVP = 100,
            APC = 1,
            TMS = 100,
            COGS = 100,
            COGS1s = 100,
            FC =200
        )
        pprint(response_data)
    except ValueError:
        print("Пожалуйста, введите корректный числовой ID.")


if __name__ == "__main__":
    asyncio.run(main())