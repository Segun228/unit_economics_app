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

from app.keyboards import inline_user as inline_keyboards

from app.states.states import Unit, Set, Send, File, UnitEdit

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

#===========================================================================================================================
# Конфигурация основных маршрутов
#===========================================================================================================================


@router.message(CommandStart(), IsAdmin())
async def cmd_start_admin(message: Message, state: FSMContext):
    data = await login(telegram_id=message.from_user.id)
    if data is None:
        logging.error("Error while logging in")
        await message.answer("Бот еще не проснулся, попробуйте немного подождать 😔", reply_markup=inline_keyboards.restart)
        return
    await state.update_data(telegram_id = data.get("telegram_id"))
    await message.reply("Приветствую Админ! 👋")
    await message.answer("Я ваш персональный финансист. Я помогу вам рассчитать юнит-экономику вашего стартапа, выбрать прибыльную стратугию, а также составить визуализацию и отчетность (чтоб инвесторы вас не съели)")
    await message.answer("Сейчас ты можешь создавать, удалять и изменять как наборы моделей (программы), так и отдельные модели юнит-экономики")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
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
# Каталог
#===========================================================================================================================
@router.callback_query(F.data == "catalogue")
async def catalogue_callback_admin(callback: CallbackQuery):
    categories = await get_sets(telegram_id=callback.from_user.id)
    await callback.message.answer("Вот доступные проекты (наборы моделей экономики)👇", reply_markup= await get_catalogue(categories=categories, telegram_id=callback.from_user.id))
    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def category_catalogue_callback_admin(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split("_")[1]
    categories = await get_sets(telegram_id=callback.from_user.id)
    print(category_id)
    current_category = None
    if categories is not None:
        for category in categories:
            if str(category.get("id")) == str(category_id):
                current_category = category
                break
    
    if current_category is None or current_category.get("units") is None or current_category.get("units") == []:
        await callback.message.answer("Извините, тут пока пусто, возвращаейтесь позже!", reply_markup= await get_posts(posts=current_category.get("units"), category=current_category ))
        await callback.answer()
        return
    await callback.message.answer("Вот доступные модели юнит-экономики👇", reply_markup= await get_posts(category= current_category ,posts = current_category.get("units", [])))


@router.callback_query(F.data.startswith("post_"))
async def post_catalogue_callback_admin(callback: CallbackQuery):
    await callback.answer()
    post_id = callback.data.split("_")[2]
    category_id = callback.data.split("_")[1]
    post_data = await get_post(
        telegram_id=callback.from_user.id,
        post_id=post_id,
        category_id=category_id
    )
    if not post_data:
        await callback.message.answer("Извините, не удалось получить доступ к позиции", reply_markup=inline_keyboards.home)
        return

    message_text = (
        f"📦 **Информация об юните:**\n\n"
        f"**Название:** `{post_data.get('name')}`\n"
        f"**Users:** `{post_data.get('users')}`\n"
        f"**Customers:** `{post_data.get('customers')}`\n"
        f"**AVP:** `{post_data.get('AVP')}`\n"
        f"**APC:** `{post_data.get('APC')}`\n"
        f"**TMS:** `{post_data.get('TMS')}`\n"
        f"**COGS:** `{post_data.get('COGS')}`\n"
        f"**COGS1s:** `{post_data.get('COGS1s')}`\n"
        f"**FC:** `{post_data.get('FC')}`\n"
    )

    await callback.message.answer(
        text=message_text,
        parse_mode="MarkdownV2",
        reply_markup=await inline_keyboards.get_post_menu(
            category_id=category_id,
            post_id=post_id,
        )
    )

#===========================================================================================================================
# Создание сета
#===========================================================================================================================


@router.callback_query(F.data == "create_category")
async def category_create_callback_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Введите название набора моделей экономики")
    await state.set_state(Set.handle_set)
    await callback.answer()


@router.message(Set.handle_set)
async def category_create_callback_admin_description(message: Message, state: FSMContext):
    name = (message.text).strip()
    await state.update_data(name = name)
    await message.answer("Введите описание набора моделей экономики")
    await state.set_state(Set.description)


@router.message(Set.description)
async def category_enter_name_admin(message: Message, state: FSMContext):
    description = (message.text).strip()
    data = await state.get_data()
    name = data.get("name")
    response = await post_set(telegram_id=message.from_user.id, name=name, description= description)
    if not response:
        await message.answer("Извините, не удалось создать набор моделей", reply_markup=inline_keyboards.main)
        return
    await message.answer("Набор моделей создан!", reply_markup= await get_catalogue(telegram_id = message.from_user.id))
    await state.clear()


#===========================================================================================================================
# Создание юнита
#===========================================================================================================================
@router.callback_query(F.data.startswith("create_post_"))
async def post_create_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    category_id = callback.data.split("_")[2]
    await state.update_data(model_set=category_id)
    await callback.message.answer("Введите название модели")
    await state.set_state(Unit.name)


@router.message(Unit.name)
async def post_enter_name_admin(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Введите валидное имя модели")
        return
    await state.update_data(name=name)
    await state.set_state(Unit.users)
    await message.answer("Введите количество привлеченных пользователей")


@router.message(Unit.users)
async def post_enter_description_admin(message: Message, state: FSMContext):
    users = message.text.strip()
    if not users.isdigit():
        await message.answer("Введите валидное число привлеченных пользователей")
        return
    await state.update_data(users=int(users))
    await state.set_state(Unit.customers)
    await message.answer("Введите количество полученных клиентов")


@router.message(Unit.customers)
async def post_enter_price_admin(message: Message, state: FSMContext):
    customers = message.text.strip()
    if not customers.isdigit():
        await message.answer("Введите валидное число полученных клиентов")
        return
    await state.update_data(customers=int(customers))
    await state.set_state(Unit.AVP)
    await message.answer("Введите AVP (Average Value of Payment)")


@router.message(Unit.AVP)
async def post_enter_country_admin(message: Message, state: FSMContext):
    avp = message.text.strip()
    if not avp.isdigit():
        await message.answer("Введите валидное число AVP (Average Value of Payment)")
        return
    await state.update_data(AVP=int(avp))
    await state.set_state(Unit.APC)
    await message.answer("Введите APC (Average Purchase Count)")


@router.message(Unit.APC)
async def post_enter_apc_admin(message: Message, state: FSMContext):
    apc = message.text.strip()
    if not apc.isdigit():
        await message.answer("Введите валидное число APC (Average Purchase Count)")
        return
    await state.update_data(APC=int(apc))
    await state.set_state(Unit.TMS)
    await message.answer("Введите TMS (Total Marketing Spends)")


@router.message(Unit.TMS)
async def post_enter_tms_admin(message: Message, state: FSMContext):
    tms = message.text.strip()
    if not tms.isdigit():
        await message.answer("Введите валидное число TMS (Total Marketing Spends)")
        return
    await state.update_data(TMS=int(tms))
    await state.set_state(Unit.COGS)
    await message.answer("Введите COGS (Cost of goods sold)")


@router.message(Unit.COGS)
async def post_enter_cogs_admin(message: Message, state: FSMContext):
    cogs = message.text.strip()
    if not cogs.isdigit():
        await message.answer("Введите валидное число COGS (Cost of goods sold)")
        return
    await state.update_data(COGS=int(cogs))
    await state.set_state(Unit.COGS1s)
    await message.answer("Введите COGS1s (Cost of goods sold first sale)")


@router.message(Unit.COGS1s)
async def post_enter_cogs1s_admin(message: Message, state: FSMContext):
    cogs1s = message.text.strip()
    if not cogs1s.isdigit():
        await message.answer("Введите валидное число COGS1s (Cost of goods sold first sale)")
        return
    await state.update_data(COGS1s=int(cogs1s))
    await state.set_state(Unit.FC)
    await message.answer("Введите FC (Fixed Costs)")


@router.message(Unit.FC)
async def post_enter_fc_admin(message: Message, state: FSMContext):
    fc = message.text.strip()
    if not fc.isdigit():
        await message.answer("Введите валидное число FC (Fixed Costs)")
        return

    await state.update_data(FC=int(fc))
    data = await state.get_data()
    unit_data = await post_post(
        telegram_id=message.from_user.id,
        category_id=data.get("model_set"),
        name=data.get("name"),
        users=data.get("users"),
        customers=data.get("customers"),
        AVP=data.get("AVP"),
        APC=data.get("APC"),
        TMS=data.get("TMS"),
        COGS=data.get("COGS"),
        COGS1s=data.get("COGS1s"),
        FC=data.get("FC"),
    )
    if not unit_data:
        await message.answer("Ошибка при создании юнита", reply_markup=await get_catalogue(message.from_user.id))
        return

    msg = (
        f"🧩 **Модель успешно создана:**\n\n"
        f"**Название:** `{unit_data.get('name')}`\n"
        f"**Пользователи:** `{unit_data.get('users')}`\n"
        f"**Клиенты:** `{unit_data.get('customers')}`\n"
        f"**AVP:** `{unit_data.get('AVP')}`\n"
        f"**APC:** `{unit_data.get('APC')}`\n"
        f"**TMS:** `{unit_data.get('TMS')}`\n"
        f"**COGS:** `{unit_data.get('COGS')}`\n"
        f"**COGS1s:** `{unit_data.get('COGS1s')}`\n"
        f"**FC:** `{unit_data.get('FC')}`"
    )
    await message.answer(msg, parse_mode="MarkdownV2", reply_markup=await inline_keyboards.get_post_menu(category_id=data.get("model_set"), post_id=unit_data.get("id")))
    await state.clear()

#===========================================================================================================================
# Редактирование сета
#===========================================================================================================================
@router.callback_query(F.data.startswith("edit_category_"))
async def category_edit_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    category_id = callback.data.split("_")[2]
    await state.set_state(Set.handle_edit_set)
    await state.update_data(category_id = category_id)
    await callback.message.answer("Введите новое название сета")


@router.message(Set.handle_edit_set)
async def category_edit_callback_admin_description(message: Message, state: FSMContext):
    name = (message.text).strip()
    await state.update_data(name = name)
    await message.answer("Введите новое описание набора моделей экономики")
    await state.set_state(Set.edit_description)


@router.message(Set.edit_description)
async def category_edit_name_admin(message: Message, state: FSMContext):
    data = await state.get_data()
    category_id = data.get("category_id")
    name = data.get("name")
    description = (message.text).strip()
    response = await put_set(telegram_id=message.from_user.id, name=name, category_id=category_id, description=description)
    if not response:
        await message.answer("Извините, не удалось отредактировать сет", reply_markup=inline_keyboards.main)
        return
    await message.answer("Сет отредактирован!", reply_markup=await get_catalogue(telegram_id = message.from_user.id))
    await state.clear()

#===========================================================================================================================
# Редактирование поста
#===========================================================================================================================
@router.callback_query(F.data.startswith("edit_post_"))
async def post_edit_callback_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    category_id, unit_id = callback.data.split("_")[2:]
    await state.update_data(category_id=category_id)
    await state.update_data(post_id=unit_id)
    await callback.message.answer("Введите новое название модели")
    await state.set_state(UnitEdit.handle_edit_unit)


@router.message(UnitEdit.handle_edit_unit)
async def post_edit_name_admin(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Введите валидное имя модели")
        return
    await state.update_data(name=name)
    await state.set_state(UnitEdit.users)
    await message.answer("Введите значение users")


@router.message(UnitEdit.users)
async def post_edit_users_admin(message: Message, state: FSMContext):
    users = message.text.strip()
    if not users.isdigit():
        await message.answer("Введите валидное число пользователей")
        return
    await state.update_data(users=int(users))
    await state.set_state(UnitEdit.customers)
    await message.answer("Введите значение customers")


@router.message(UnitEdit.customers)
async def post_edit_customers_admin(message: Message, state: FSMContext):
    customers = message.text.strip()
    if not customers.isdigit():
        await message.answer("Введите валидное число клиентов")
        return
    await state.update_data(customers=int(customers))
    await state.set_state(UnitEdit.AVP)
    await message.answer("Введите значение AVP")


@router.message(UnitEdit.AVP)
async def post_edit_avp_admin(message: Message, state: FSMContext):
    avp = message.text.strip()
    if not avp.isdigit():
        await message.answer("Введите валидное значение AVP")
        return
    await state.update_data(AVP=int(avp))
    await state.set_state(UnitEdit.APC)
    await message.answer("Введите значение APC")


@router.message(UnitEdit.APC)
async def post_edit_apc_admin(message: Message, state: FSMContext):
    apc = message.text.strip()
    if not apc.isdigit():
        await message.answer("Введите валидное значение APC")
        return
    await state.update_data(APC=int(apc))
    await state.set_state(UnitEdit.TMS)
    await message.answer("Введите значение TMS")


@router.message(UnitEdit.TMS)
async def post_edit_tms_admin(message: Message, state: FSMContext):
    tms = message.text.strip()
    if not tms.isdigit():
        await message.answer("Введите валидное значение TMS")
        return
    await state.update_data(TMS=int(tms))
    await state.set_state(UnitEdit.COGS)
    await message.answer("Введите значение COGS")


@router.message(UnitEdit.COGS)
async def post_edit_cogs_admin(message: Message, state: FSMContext):
    cogs = message.text.strip()
    if not cogs.isdigit():
        await message.answer("Введите валидное значение COGS")
        return
    await state.update_data(COGS=int(cogs))
    await state.set_state(UnitEdit.COGS1s)
    await message.answer("Введите значение COGS1s")


@router.message(UnitEdit.COGS1s)
async def post_edit_cogs1s_admin(message: Message, state: FSMContext):
    cogs1s = message.text.strip()
    if not cogs1s.isdigit():
        await message.answer("Введите валидное значение COGS1s")
        return
    await state.update_data(COGS1s=int(cogs1s))
    await state.set_state(UnitEdit.FC)
    await message.answer("Введите значение FC")


@router.message(UnitEdit.FC)
async def post_edit_fc_admin(message: Message, state: FSMContext):
    fc = message.text.strip()
    if not fc.isdigit():
        await message.answer("Введите валидное значение FC")
        return

    data = await state.get_data()
    logging.warning(f"DATA: {data}")
    unit_data = await put_post(
        telegram_id=message.from_user.id,
        category_id=data.get("category_id"),
        name=data.get("name"),
        users=data.get("users"),
        customers=data.get("customers"),
        AVP=data.get("AVP"),
        APC=data.get("APC"),
        TMS=data.get("TMS"),
        COGS=data.get("COGS"),
        COGS1s=data.get("COGS1s"),
        FC=int(fc),
        post_id=data.get("post_id")
    )

    if not unit_data:
        await message.answer("Ошибка при обновлении модели", reply_markup=await get_catalogue(telegram_id=message.from_user.id))
        return

    await message.answer("Модель успешно обновлена")
    message_text = (
        f"🔧 **Обновлённая модель:**\n\n"
        f"**Название:** `{unit_data.get('name')}`\n"
        f"**Users:** `{unit_data.get('users')}`\n"
        f"**Customers:** `{unit_data.get('customers')}`\n"
        f"**AVP:** `{unit_data.get('AVP')}`\n"
        f"**APC:** `{unit_data.get('APC')}`\n"
        f"**TMS:** `{unit_data.get('TMS')}`\n"
        f"**COGS:** `{unit_data.get('COGS')}`\n"
        f"**COGS1s:** `{unit_data.get('COGS1s')}`\n"
        f"**FC:** `{unit_data.get('FC')}`"
    )

    await message.answer(
        message_text,
        reply_markup=await inline_keyboards.get_post_menu(
            category_id=data.get("category_id"),
            post_id=data.get("post_id")
        ),
        parse_mode="MarkdownV2"
    )
    await state.clear()
#===========================================================================================================================
# Удаление сета   
#===========================================================================================================================

@router.callback_query(F.data.startswith("delete_category_"))
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

@router.callback_query(F.data.startswith("delete_post_"))
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
# Разрешение доступа
#===========================================================================================================================


@router.callback_query(F.data.startswith("access_give"))
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


@router.callback_query(F.data.startswith("access_reject"))
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


@router.callback_query(F.data == "file_panel")
async def file_panel_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    await callback.message.edit_text(
        "Выберите интересующую функцию",
        reply_markup= inline_keyboards.file_panel
    )


@router.callback_query(F.data == "get_report")
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



@router.callback_query(F.data == "add_posts")
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


@router.message(File.waiting_for_file)
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


@router.callback_query(F.data == "replace_posts")
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


@router.message(File.waiting_for_replace_file)
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
