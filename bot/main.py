import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from app.handlers.router import admin_router, user_router
from app.middlewares.antiflud import ThrottlingMiddleware


from app.handlers import user_handlers
from app.handlers import admin_handlers


from app.kafka.utils import ensure_topic_exists

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("No token provided")
    raise ValueError("No token provided")

ensure_topic_exists()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(ThrottlingMiddleware(limit=0.5))
dp.include_router(admin_router)
dp.include_router(user_router)

async def main():
    logging.info("Starting bot with long polling...")
    try:
        await dp.start_polling(bot)
    finally:
        logging.info("Shutting down bot...")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())