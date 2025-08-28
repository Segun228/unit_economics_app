from app.handlers.router import admin_router as router
import logging
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from typing import Dict, Any
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from aiogram.exceptions import TelegramAPIError
from io import BytesIO
import asyncio

from aiogram.types import InputFile

from app.keyboards import inline_admin as inline_keyboards

from app.states.states import Unit, Send, File, Set

from aiogram.types import BufferedInputFile


from app.keyboards.inline_user import get_catalogue, get_posts

from app.filters.IsAdmin import IsAdmin

from app.requests.user.login import login
from app.requests.helpers.get_cat_error import get_cat_error_async
from app.requests.get.get_sets import get_sets
from app.requests.get.get_post import get_post

from app.requests.helpers.get_cat_error import get_cat_error_async

from app.requests.post.postCategory import post_set
from app.requests.post.postPost import post_post
from app.requests.put.putCategory import put_set
from app.requests.put.putPost import put_post
from app.requests.delete.deleteCategory import delete_category
from app.requests.delete.deletePost import delete_post
from app.requests.user.get_alive import get_alive
from app.requests.user.make_admin import make_admin

from app.requests.files.get_report import get_report
from app.requests.files.put_report import put_report

from app.kafka.utils import build_log_message
#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================


@router.message(CommandStart())
async def cmd_start_admin(message: Message, state: FSMContext):
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Бот еще не проснулся, попробуйте немного подождать 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Приветствую! 👋")
    await message.answer("Я ваш персональный финансист. Я помогу вам рассчитать юнит-экономику вашего стартапа, выбрать прибыльную стратугию, а также составить визуализацию и отчетность (чтоб инвесторы вас не съели)")
    await message.answer("Сейчас ты можешь создавать, удалять и изменять как наборы моделей (программы), так и отдельные модели юнит-экономики")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    build_log_message(
        telegram_id=message.from_user.id,
        action="command",
        source="command",
        payload="start"
    )
    await state.clear()


@router.callback_query(F.data == "restart")
async def callback_start_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Бот еще не проснулся, попробуйте немного подождать 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет, админ! 👋")
    await callback.message.answer("Я ваш персональный финансист. Я помогу вам рассчитать юнит-экономику вашего стартапа, выбрать прибыльную стратугию, а также составить визуализацию и отчетность (чтоб инвесторы вас не съели)")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    build_log_message(
        telegram_id=callback.from_user.id,
        action="inline",
        source="callback",
        payload="restart"
    )
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот помогает рассчитывать юнит экономику, подбирать метрики для заданной прибыли или окупаемости, а также проссчитывать необходимое кол-во юнитов и точку безубыточности\n\n Он может выполнять несколько интересных функций \n\nВы можете выбирать интересующие вас функции, в каждой из них вам будут предоставлены инструкции\n\nЕсли у вас остались вопросы, звоните нам или пишите в тех поддержку, мы всегда на связи:\n\nтелефон коммерческого агента\n\n@dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с менеджером: 📞\n\n\\тут телефон коммерческого агента\n\n"+"Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    text = "Связь с менеджером: 📞\n\n\\тут телефон коммерческого агента\n\n"+"Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

#===========================================================================================================================
# Создание рассылки
#===========================================================================================================================

@router.callback_query(F.data == "send_menu", IsAdmin())
async def send_menu_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Send.handle)
    await callback.message.answer(
        "Извините, вы не обладаете достаточными правами",
        reply_markup=inline_keyboards.catalogue
    )
    return


@router.callback_query(F.data == "send_menu", IsAdmin())
async def send_menu_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Напишите текст сообщения или прикрепите фото с подписью. ",
        reply_markup=inline_keyboards.catalogue
    )
    


@router.message(Send.handle, F.photo, IsAdmin())
async def send_photo_message(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    caption = message.caption or ""
    await state.update_data(photo=photo, caption=caption)
    await message.answer("Фото получено. Начинаю рассылку...")
    await start_broadcast(state, message, message.bot)


@router.message(Send.handle, F.text, IsAdmin())
async def send_text_message(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Текст получен. Начинаю рассылку...")
    await start_broadcast(state, message, message.bot)


async def start_broadcast(state: FSMContext, message: Message, bot: Bot):
    data = await state.get_data()
    users_data = await get_alive(telegram_id=message.from_user.id)

    if not users_data:
        await message.answer("Ошибка при рассылке. Попробуйте позже.")
        await state.clear()
        return

    tasks = []
    for user in users_data:
        user_id = user.get("telegram_id")
        if "photo" in data:
            tasks.append(
                bot.send_photo(chat_id=user_id, photo=data["photo"], caption=data.get("caption", ""))
            )
        elif "text" in data:
            tasks.append(
                bot.send_message(chat_id=user_id, text=data["text"])
            )

    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful_sends = sum(1 for r in results if not isinstance(r, TelegramAPIError))
    failed_sends = len(results) - successful_sends

    await message.answer(
        f"Рассылка завершена.\n✅ Успешно: {successful_sends}\n❌ Ошибки: {failed_sends}",
        reply_markup=inline_keyboards.main
    )
    await state.clear()

#===========================================================================================================================
# Разрешение доступа
#===========================================================================================================================


@router.callback_query(F.data.startswith("access_give"), IsAdmin())
async def give_acess_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    request = str(callback.data)
    try:
        user_id = list(request.split("_"))[2]
        if not user_id:
            logging.error("Ошибка предоставления доступа")
            return
        response = await make_admin(
            telegram_id= callback.from_user.id,
            target_user_id= user_id
        )
        if not response:
            logging.error("Ошибка предоставления доступа")
            await bot.send_message(chat_id=int(user_id), text="К сожалению, вам было отказано в предоставлении прав администратора", reply_markup=inline_keyboards.home)
        else:
            logging.info(response)
            await callback.message.answer("Права администратора были успешно предоставлены", reply_markup=inline_keyboards.home)
            await bot.send_message(chat_id=user_id, text="Вам были предоставлены права администратора", reply_markup=inline_keyboards.home)
    except Exception as e:
        logging.error(e)


@router.callback_query(F.data.startswith("access_reject"), IsAdmin())
async def reject_acess_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    request = str(callback.data)
    try:
        user_id = list(request.split("_"))[2]
        await bot.send_message(chat_id=int(user_id), text="К сожалению, вам было отказано в предоставлении прав администратора", reply_markup=inline_keyboards.home)
    except Exception as e:
        logging.error(e)



#===========================================================================================================================
# Файловое меню
#===========================================================================================================================


@router.callback_query(F.data == "file_panel", IsAdmin())
async def file_panel_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    await callback.message.edit_text(
        "Выберите интересующую функцию",
        reply_markup= inline_keyboards.file_panel
    )


@router.callback_query(F.data == "get_report", IsAdmin())
async def send_report_admin(callback: CallbackQuery, state: FSMContext, bot: Bot):

    await callback.answer("Готовлю ваш отчёт...", show_alert=False)
    docs = await get_report(telegram_id=callback.from_user.id)

    if not docs:
        await callback.message.answer("Извините, не удалось загрузить отчёт. Обратитесь в поддержку.")
        return

    await callback.message.answer(
        "Вот ваш отчёт!"
    )

    await bot.send_document(
        chat_id=callback.message.chat.id,
        document=BufferedInputFile(docs.getvalue(), filename="report.xlsx"),
        reply_markup=inline_keyboards.file_panel
    )
    await state.clear()



@router.callback_query(F.data == "add_posts", IsAdmin())
async def file_add_posts_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    await callback.message.answer(
        "Это текущие позиции"
    )
    docs = await get_report(telegram_id=callback.from_user.id)
    await bot.send_document(
        chat_id=callback.message.chat.id,
        document=BufferedInputFile(docs.getvalue(), filename="report.xlsx"),
    )
    await callback.message.answer(
        "Вы в режиме добавления позиций. Отправте в чат файл с позициями, которые хотите добавить, в том же формате"
    )
    await state.set_state(File.waiting_for_file)


@router.message(File.waiting_for_file, IsAdmin())
async def upload_add_file_admin(message: Message, state: FSMContext, bot: Bot):
    try:

        file = await bot.get_file(message.document.file_id)
        file_bytes = await bot.download_file(file.file_path)
        response = await put_report(message.from_user.id, file_bytes)


        if not response:
            await message.answer(
                "К сожалению, не удалось обработать файл. Убедитесь, что формат файла соответствует установленному."
            )
            await state.clear()
            return
        await message.answer("Файл успешно получен и обработан!", reply_markup= inline_keyboards.file_panel)
        await state.clear()

    except Exception as e:
        await state.clear()
        logging.error(f"Ошибка при обработке Excel: {e}")
        await message.answer("Не удалось обработать файл. Убедитесь, что это корректный Excel (.xlsx).", reply_markup= inline_keyboards.file_panel)


@router.callback_query(F.data == "replace_posts", IsAdmin())
async def file_replace_posts_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    await callback.message.answer(
        "Это текущие позиции"
    )
    docs = await get_report(telegram_id=callback.from_user.id)
    await bot.send_document(
        chat_id=callback.message.chat.id,
        document=BufferedInputFile(docs.getvalue(), filename="report.xlsx"),
    )
    await callback.message.answer(
        "Вы в режиме полного обновления позиций. Отправте в чат файл с позициями, которые хотите добавить, в том же формате. Будте внимательны, текущие позиции будут удалены"
    )
    await state.set_state(File.waiting_for_replace_file)


@router.message(File.waiting_for_replace_file, IsAdmin())
async def upload_replace_file_admin(message: Message, state: FSMContext, bot: Bot):
    try:
        file = await bot.get_file(message.document.file_id)
        file_bytes = await bot.download_file(file.file_path)
        response = await replace_report(message.from_user.id, file_bytes)
        if not response:
            await message.answer(
                "К сожалению, не удалось обработать файл. Убедитесь, что формат файла соответствует установленному."
            )
            await state.clear()
            return
        await message.answer("Файл успешно получен и обработан! Позиции обновлены", reply_markup= inline_keyboards.file_panel)
        await state.clear()

    except Exception as e:
        logging.error(f"Ошибка при обработке Excel: {e}")
        await state.clear()
        await message.answer("Не удалось обработать файл. Убедитесь, что это корректный Excel (.xlsx).", reply_markup= inline_keyboards.file_panel)
