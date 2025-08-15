from app.handlers.router import user_router as router
import asyncio
import logging
import random
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from typing import Dict, Any
from aiogram.fsm.context import FSMContext

from app.keyboards import inline_user as inline_keyboards

from app.states.states import Post

from aiogram.types import BufferedInputFile

from app.keyboards.inline_user import get_catalogue, get_posts

from app.requests.user.login import login
from app.requests.user.set_blocked import set_blocked
from app.requests.helpers.get_cat_error import get_cat_error_async
from app.requests.get.get_categories import get_categories
from app.requests.get.get_post import get_post
from app.requests.helpers.get_cat_error import get_cat_error_async
from aiogram.filters import ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated

from app.filters.IsAdmin import IsAdmin


#===========================================================================================================================
# Валидация блокировки пользователя
#===========================================================================================================================
"""
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    await set_blocked(telegram_id=event.from_user.id, value=False)
"""
#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================

@router.message(CommandStart(), ~IsAdmin())
async def cmd_start(message: Message, state: FSMContext):
    data = await login(telegram_id=message.from_user.id)
    await set_blocked(telegram_id=message.from_user.id, value=True)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Привет, пользователь! 👋")
    await message.reply("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await state.clear()


@router.callback_query(F.data == "restart")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет! 👋")
    await callback.message.reply("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот помогает выбирать экзотические растения из нужных категорий\n\n Он может выполнять несколько интересных функций \n\nВы можете выбирать интересующие вас растения из категорий, имеющихся в наличии\n\nЕсли остались вопросы, пиши нашим менеджерам:\n\n@Elena_Noro\n\n@dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с менеджером: 📞\n\n\\@Elena\\_Noro\n\n"+"Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback: CallbackQuery):
    text = "Связь с менеджером: 📞\n\n\\@Elena\\_Noro\n\n"+"Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

#===========================================================================================================================
# Каталог
#===========================================================================================================================
@router.callback_query(F.data == "catalogue")
async def catalogue_callback(callback: CallbackQuery):
    categories = await get_categories(telegram_id= callback.from_user.id)
    await callback.message.answer("Вот доступные категории👇", reply_markup= await get_catalogue(categories))
    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def category_catalogue_callback(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split("_")[1]
    categories = await get_categories(telegram_id= callback.from_user.id)
    print(category_id)
    current_category = None
    if categories is not None:
        for category in categories:
            if str(category.get("id")) == str(category_id):
                current_category = category
                break
    
    if current_category is None or current_category.get("posts") is None or current_category.get("posts") == []:
        await callback.message.answer("Извините, тут пока пусто, возвращаейтесь позже! ⏳", reply_markup= inline_keyboards.catalogue)
        await callback.answer()
        return
    await callback.message.answer("Вот доступные предложения👇", reply_markup= await get_posts(category= current_category ,posts = current_category.get("posts", [])))


@router.callback_query(F.data.startswith("post_"))
async def post_catalogue_callback(callback: CallbackQuery):
    await callback.answer()
    post_id = callback.data.split("_")[2]
    category_id = callback.data.split("_")[1]
    post_data = await get_post(
        telegram_id=callback.from_user.id,
        post_id= post_id,
        category_id= category_id
    )
    if post_data is None or not post_data:
        await callback.message.answer("Извините, не удалось получить доступ к объявлению 😔", reply_markup=inline_keyboards.home)
        return
    await send_post_photos(callback = callback, post = post_data)
    message_text = (
        f"📝 **Информация о товаре:**\n"
        f"**Название:** `{post_data['title']}`\n"
        f"**Описание:** `{post_data['description']}`\n"
        f"**Цена:** `{post_data['price']}`\n"
        f"**Количество:** `{post_data['quantity']}`\n"
    )
    await callback.message.answer(
        text=message_text,
        parse_mode="MarkdownV2",
        reply_markup=inline_keyboards.home
    )
#===========================================================================================================================
# Взаимодействие с аккаунтом
#===========================================================================================================================
@router.callback_query(F.data == "account_menu")
async def account_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text("Что вы хотите сделать с вашим аккаунтом? 👤", reply_markup=inline_keyboards.account_menu)
    await callback.answer()

@router.callback_query(F.data == "delete_account_confirmation")
async def delete_account_confirmation_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вы уверены что хотите удалить аккаунт? 😳 Восстановить записи будет невозможно... 🗑️", reply_markup=inline_keyboards.delete_account_confirmation_menu)
    await callback.answer()

@router.callback_query(F.data == "delete_account")
async def delete_account_callback(callback: CallbackQuery, state: FSMContext):
    await delete_account(telegram_id=callback.from_user.id)
    await state.clear()
    await callback.message.edit_text("Аккаунт удален 😢", reply_markup=inline_keyboards.restart)
    await callback.answer()


#===========================================================================================================================
# Заглушка
#===========================================================================================================================

@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    photo_data = await get_cat_error_async()
    if photo_data:
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo_to_send)


async def send_post_photos(callback: CallbackQuery, post: Dict[str, Any]):
    photo_ids = post.get('photos', [])

    if not photo_ids:
        await callback.message.answer("К сожалению, у этого поста нет фотографий. 🖼️")
        return

    first_photo_id = photo_ids[0]
    caption_text = f"**{post.get('title', 'Без названия')}**"
    
    await callback.message.answer_photo(
        photo=first_photo_id,
        caption=caption_text,
        parse_mode="MarkdownV2"
    )

    for photo_id in photo_ids[1:]:
        await callback.message.answer_photo(photo=photo_id)