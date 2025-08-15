from app.handlers.router import admin_router as router
import logging
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from typing import Dict, Any
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from aiogram.exceptions import TelegramAPIError
import asyncio

from app.keyboards import inline_admin as inline_keyboards

from app.states.states import Post, Category, Send

from aiogram.types import BufferedInputFile

from app.keyboards.inline_admin import get_catalogue, get_posts

from app.filters.IsAdmin import IsAdmin

from app.requests.user.login import login
from app.requests.helpers.get_cat_error import get_cat_error_async
from app.requests.get.get_categories import get_categories
from app.requests.get.get_post import get_post
from app.requests.post.postPhotos import post_photos
from app.requests.helpers.get_cat_error import get_cat_error_async

from app.requests.post.postCategory import post_category
from app.requests.post.postPost import post_post
from app.requests.put.putCategory import put_category
from app.requests.put.putPost import put_post
from app.requests.delete.deleteCategory import delete_category
from app.requests.delete.deletePost import delete_post
from app.requests.user.get_alive import get_alive
#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================


@router.message(CommandStart(), IsAdmin())
async def cmd_start_admin(message: Message, state: FSMContext):
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Ошибка админской авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Привет, админ! 👋")
    await message.answer("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await message.answer("Сейчас ты можешь создавать, удалять и изменять как категории, так и объявления")
    await message.answer("Также ты можешь активировать расслыку по активным пользователям")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await state.clear()


@router.callback_query(F.data == "restart", IsAdmin())
async def callback_start_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = await login(telegram_id=callback.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await callback.message.answer("Ошибка авторизации, попробуйте позже 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await callback.message.reply("Привет, админ! 👋")
    await callback.message.reply("Я бот платформы Florilegium. Я помогу вам выбрать и заказать лучшие экзотические растения")
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()


@router.message(Command("help"), IsAdmin())
async def cmd_help_admin(message: Message):
    await message.reply(text="Этот бот помогает выбирать экзотические растения из нужных категорий\n\n Он может выполнять несколько интересных функций \n\nВы можете выбирать интересующие вас растения из категорий, имеющихся в наличии\n\nЕсли остались вопросы, пиши нашим менеджерам:\n\n@Elena_Noro\n\n@dianabol_metandienon_enjoyer", reply_markup=inline_keyboards.home)

@router.message(Command("contacts"), IsAdmin())
async def cmd_contacts_admin(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "contacts", IsAdmin())
async def contacts_callback_admin(callback: CallbackQuery):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu", IsAdmin())
async def main_menu_callback_admin(callback: CallbackQuery):
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

#===========================================================================================================================
# Каталог
#===========================================================================================================================
@router.callback_query(F.data == "catalogue", IsAdmin())
async def catalogue_callback_admin(callback: CallbackQuery):
    categories = await get_categories(telegram_id= callback.from_user.id)
    await callback.message.answer("Вот доступные категории👇", reply_markup= await get_catalogue(categories= categories, telegram_id=callback.from_user.id))
    await callback.answer()


@router.callback_query(F.data.startswith("category_"), IsAdmin())
async def category_catalogue_callback_admin(callback: CallbackQuery):
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
        await callback.message.answer("Извините, тут пока пусто, возвращаейтесь позже!", reply_markup= await get_posts(posts=current_category.get("posts"), category=current_category ))
        await callback.answer()
        return
    await callback.message.answer("Вот доступные предложения👇", reply_markup= await get_posts(category= current_category ,posts = current_category.get("posts", [])))


@router.callback_query(F.data.startswith("post_"), IsAdmin())
async def post_catalogue_callback_admin(callback: CallbackQuery):
    await callback.answer()
    post_id = callback.data.split("_")[2]
    category_id = callback.data.split("_")[1]
    post_data = await get_post(
        telegram_id=callback.from_user.id,
        post_id= post_id,
        category_id= category_id
    )
    if post_data is None or not post_data:
        await callback.message.answer("Извините, не удалось получить доступ к объявлению", reply_markup=inline_keyboards.home)
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
        reply_markup= await inline_keyboards.get_post_menu(
            category_id= category_id,
            post_id= post_id,
        )
    )
#===========================================================================================================================
# Поддержка
#===========================================================================================================================


async def send_post_photos(callback: CallbackQuery, post: Dict[str, Any]):
    photo_ids = post.get('photos', [])

    if not photo_ids:
        await callback.message.answer("К сожалению, у этого поста нет фотографий.")
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

#===========================================================================================================================
# Создание категории
#===========================================================================================================================


@router.callback_query(F.data == "create_category", IsAdmin())
async def category_create_callback_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Введите название категории")
    await state.set_state(Category.handle_category)
    await callback.answer()

@router.message(Category.handle_category, IsAdmin())
async def category_enter_name_admin(message: Message, state: FSMContext):
    name = (message.text).strip()
    response = await post_category(telegram_id=message.from_user.id, title=name)
    if not response:
        await message.answer("Извините, не удалось создать категорию", reply_markup=inline_keyboards.main)
        return
    await message.answer("Категория создана!", reply_markup= await get_catalogue(telegram_id = message.from_user.id))
    await state.clear()


#===========================================================================================================================
# Создание поста
#===========================================================================================================================


@router.callback_query(F.data.startswith("create_post_"), IsAdmin())
async def post_create_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    catergory_id = callback.data.split("_")[2]
    await state.update_data(category = catergory_id)
    await callback.message.answer("Введите название поста")
    await state.set_state(Post.handle_post)


@router.message(Post.handle_post, IsAdmin())
async def post_enter_name_admin(message: Message, state: FSMContext):
    title = (message.text).strip()
    if not title:
        await message.answer("Введите валидное имя поста")
        return
    await state.update_data(title = title)
    await state.set_state(Post.title)
    await message.answer("Введите описание поста")


@router.message(Post.title, IsAdmin())
async def post_enter_description_admin(message: Message, state: FSMContext):
    description = (message.text).strip()
    if not description:
        await message.answer("Введите валидное описание поста")
        return
    await state.update_data(description=description)
    await state.set_state(Post.description)
    await message.answer("Введите цену")


@router.message(Post.description, IsAdmin())
async def post_enter_price_admin(message: Message, state: FSMContext):
    price = (message.text).strip()
    if not price or not price.isdigit():
        await message.answer("Введите валидную цену")
        return
    await state.update_data(price = price)
    await state.set_state(Post.price)
    await message.answer("Введите количество в наличии")


@router.message(Post.price, IsAdmin())
async def post_enter_quantity_admin(message: Message, state: FSMContext):
    quantity = (message.text).strip()
    if not quantity or not quantity.isdigit():
        await message.answer("Введите валидное количество")
        return
    data = await state.get_data()
    post_data = await post_post(
        telegram_id= message.from_user.id,
        category_id= data.get("category"),
        title = data.get("title"),
        description= data.get("description"),
        price = data.get("price"),
        quantity = quantity
    )
    if not post_data:
        await message.answer("Извините, ошибка при создании поста", reply_markup=await get_catalogue(telegram_id = message.from_user.id))
        return
    await message.answer("Пост успешно создан")
    message_text = (
        f"📝 **Информация о товаре:**\n"
        f"**Название:** `{post_data['title']}`\n"
        f"**Описание:** `{post_data['description']}`\n"
        f"**Цена:** `{post_data['price']}`\n"
        f"**Количество:** `{post_data['quantity']}`\n"
    )
    await message.answer(message_text, reply_markup=await inline_keyboards.get_post_menu(category_id=post_data.get("category"), post_id=post_data.get("id")), parse_mode="MarkdownV2")
    await state.clear()
#===========================================================================================================================
# Редактирование категории
#===========================================================================================================================
@router.callback_query(F.data.startswith("edit_category_"), IsAdmin())
async def category_edit_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    category_id = callback.data.split("_")[2]
    await state.set_state(Category.handle_edit_category)
    await state.update_data(category_id = category_id)
    await callback.message.answer("Введите название категории")

@router.message(Category.handle_edit_category, IsAdmin())
async def category_edit_name_admin(message: Message, state: FSMContext):
    data = await state.get_data()
    category_id = data.get("category_id")
    name = (message.text).strip()
    response = await put_category(telegram_id=message.from_user.id, title=name, category_id=category_id)
    if not response:
        await message.answer("Извините, не удалось отредактировать категорию", reply_markup=inline_keyboards.main)
        return
    await message.answer("Категория отредактирована!", reply_markup=await get_catalogue(telegram_id = message.from_user.id))
    await state.clear()

#===========================================================================================================================
# Редактирование поста
#===========================================================================================================================


@router.callback_query(F.data.startswith("edit_post_"), IsAdmin())
async def post_edit_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    catergory_id, post_id = callback.data.split("_")[2:]
    await state.update_data(category = catergory_id)
    await state.update_data(post_id = post_id)
    await callback.message.answer("Введите название поста")
    await state.set_state(Post.handle_edit_post)


@router.message(Post.handle_edit_post, IsAdmin())
async def post_edit_name_admin(message: Message, state: FSMContext):
    title = (message.text).strip()
    if not title:
        await message.answer("Введите валидное имя поста")
        return
    await state.update_data(title = title)
    await state.set_state(Post.title)
    await message.answer("Введите описание поста")


@router.message(Post.title, IsAdmin())
async def post_edit_description_admin(message: Message, state: FSMContext):
    description = (message.text).strip()
    if not description:
        await message.answer("Введите валидное описание поста")
        return
    await state.update_data(description=description)
    await state.set_state(Post.description)
    await message.answer("Введите цену")


@router.message(Post.description, IsAdmin())
async def post_edit_price_admin(message: Message, state: FSMContext):
    price = (message.text).strip()
    if not price or not price.isdigit():
        await message.answer("Введите валидную цену")
        return
    await state.update_data(price = price)
    await state.set_state(Post.price)
    await message.answer("Введите количество в наличии")


@router.message(Post.price, IsAdmin())
async def post_edit_quantity_admin(message: Message, state: FSMContext):
    quantity = (message.text).strip()
    if not quantity or not quantity.isdigit():
        await message.answer("Введите валидное количество")
        return
    data = await state.get_data()
    post_data = await put_post(
        telegram_id= message.from_user.id,
        category_id= data.get("category"),
        post_id = data.get("post_id"),
        title = data.get("title"),
        description= data.get("description"),
        price = data.get("price"),
        quantity = quantity
    )
    if not post_data:
        await message.answer("Извините, ошибка при обновлении поста", reply_markup=await get_catalogue(telegram_id = message.from_user.id))
        return
    await message.answer("Пост успешно обновлен")
    message_text = (
        f"📝 **Информация о товаре:**\n"
        f"**Название:** `{post_data['title']}`\n"
        f"**Описание:** `{post_data['description']}`\n"
        f"**Цена:** `{post_data['price']}`\n"
        f"**Количество:** `{post_data['quantity']}`\n"
    )
    await message.answer(message_text, reply_markup=await inline_keyboards.get_post_menu(category_id=data.get("category"), post_id=data.get("post_id")), parse_mode="MarkdownV2")
    await state.clear()

#===========================================================================================================================
# Удаление категории
#===========================================================================================================================

@router.callback_query(F.data.startswith("delete_category_"), IsAdmin())
async def category_delete_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    category_id = callback.data.split("_")[2]
    response = await delete_category(telegram_id=callback.from_user.id, category_id=category_id)
    if not response:
        await callback.message.answer("Извините, не удалось удалить категорию", reply_markup=inline_keyboards.main)
        return
    await callback.message.answer("Категория удалена!", reply_markup=await get_catalogue(telegram_id = callback.from_user.id))
    await state.clear()


#===========================================================================================================================
# Удаление поста
#===========================================================================================================================

@router.callback_query(F.data.startswith("delete_post_"), IsAdmin())
async def post_delete_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    catergory_id, post_id = callback.data.split("_")[2:]
    response = await delete_post(telegram_id=callback.from_user.id, category_id=catergory_id, post_id=post_id)
    if not response:
        await callback.message.answer("Извините, не удалось удалить пост",reply_markup= await get_catalogue(telegram_id = callback.from_user.id))
    await callback.message.answer("Пост успешно удален",reply_markup=await get_catalogue(telegram_id = callback.from_user.id))
    await state.clear()

#===========================================================================================================================
# Добавление фото
#===========================================================================================================================


@router.callback_query(F.data.startswith("add_photo_"), IsAdmin())
async def post_add_photos_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        post_id = callback.data.split("_")[2]
        await state.update_data(post_id=int(post_id))
    except (IndexError, ValueError):
        await callback.message.answer("Ошибка: неверный ID поста.", reply_markup=await get_catalogue(telegram_id= callback.from_user.id))
        await state.clear()
        return
    await callback.message.answer("Отправьте фотографии для поста. После того как закончите, напишите 'Готово'.")
    await state.set_state(Post.waiting_for_photos)


@router.message(Post.waiting_for_photos, IsAdmin(), F.photo)
async def handle_photo_upload_admin(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(photo_id)
    await state.update_data(photos=photos)
    await message.answer("Фотография добавлена. Отправьте ещё или напишите 'Готово'.")

@router.message(Post.waiting_for_photos, F.text.lower() == "готово", IsAdmin())
async def finish_photo_upload_admin(message: Message, state: FSMContext):
    data = await state.get_data()
    post_id = data.get("post_id")
    photo_ids = data.get("photos", [])
    
    if not photo_ids:
        await message.answer("Вы не отправили ни одной фотографии. Попробуйте снова.")
        return
    response = await post_photos(telegram_id= message.from_user.id ,post_id= post_id, photos= photo_ids)
    if response:
        await message.answer("Фотографии успешно добавлены к посту ID!", reply_markup=await get_catalogue(telegram_id=message.from_user.id))
    else:
        await message.answer("Извините, не удалось добавить фотографии.")
    await state.clear()


#===========================================================================================================================
# Создание рассылки
#===========================================================================================================================

@router.callback_query(F.data == "send_menu", IsAdmin())
async def send_menu_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Send.handle)
    await callback.message.answer("Напишите, какое сообщение хотите отправить всем активным пользователям. Будте внимательны, отменить рассылку будет невозможно")


@router.message(Send.handle, IsAdmin())
async def send_admin(message: Message, state: FSMContext, bot: Bot):
    text = message.text
    users_data = await get_alive(telegram_id=message.from_user.id)

    if users_data is None or text is None:
        await message.answer("Ошибка при рассылке, повторите позже", reply_markup=inline_keyboards.catalogue)
        return


    tasks = []
    for user_data in users_data:
        user_id = user_data.get("telegram_id")
        tasks.append(bot.send_message(chat_id=user_id, text=text))

    results = await asyncio.gather(*tasks, return_exceptions=True)


    successful_sends = 0
    failed_sends = 0
    for result in results:
        if isinstance(result, TelegramAPIError):
            print(f"Не удалось отправить сообщение: {result}")
            failed_sends += 1
        else:
            successful_sends += 1
    
    final_message = (
        f"Рассылка завершена. Успешно отправлено: {successful_sends}, "
        f"не отправлено: {failed_sends}."
    )
    await message.answer(final_message, reply_markup=inline_keyboards.main)
    await state.clear()