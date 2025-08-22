import aiohttp
import os
import logging
from io import BytesIO
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def put_report(telegram_id, file_bytes: bytes, name=""):
    load_dotenv()
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("No base URL")
    if not telegram_id:
        raise ValueError("No telegram_id")

    form = aiohttp.FormData()
    form.add_field(
        name='file',
        value=file_bytes, 
        filename='report.xlsx',
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    form.add_field(
        name='name',
        value=name
    )

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bot {telegram_id}"}
        exact_url = f"{base_url}analitics/file/upload/"

        async with session.post(exact_url, headers=headers, data=form) as response:
            if response.status in (200, 201, 202, 203):
                return await response.json()
            else:
                text = await response.text()
                logging.error(f"Failed: {response.status} - {text}")
                return None