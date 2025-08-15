import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.router import admin_router, user_router
import app.handlers.admin_handlers
import app.handlers.user_handlers
from app.middlewares.antiflud import ThrottlingMiddleware


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

token = os.getenv("BOT_TOKEN")
if not token or token == "":
    raise ValueError("No token was provided")

bot:Bot = Bot(token = token)
dp = Dispatcher()
dp.message.middleware(ThrottlingMiddleware(limit=0.5))
dp.include_router(admin_router)
dp.include_router(user_router)
async def main():
    try:
        logging.info("Bot started")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Bot stopped")
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)



if __name__ == "__main__":
    asyncio.run(main())
