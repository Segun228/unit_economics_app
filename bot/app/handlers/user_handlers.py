from app.handlers.router import admin_router as router
import logging
import re
import zipfile
import io
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

from app.states.states import Unit, Set, Send, File, UnitEdit, Cohort, SetCohort

from aiogram.types import BufferedInputFile


from app.keyboards.inline_user import get_catalogue, get_posts

from app.filters.IsAdmin import IsAdmin

from app.requests.user.login import login
from app.requests.helpers.get_cat_error import get_cat_error_async
from app.requests.get.get_sets import get_sets, retrieve_set
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

from app.requests.units import get_unit_report, get_unit_bep, get_unit_exel
from app.requests.put import update_model_cohort_data
from app.requests.units.get_unit_cohort import get_unit_cohort

from app.requests.sets.set_generate_report import set_generate_report
from app.requests.sets.set_visualize import set_visualize
from app.requests.sets.get_set_cohort import get_set_cohort
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
    finally:
        await state.clear()

#===========================================================================================================================
# Файловое меню
#===========================================================================================================================


@router.callback_query(F.data == "file_panel")
async def file_panel_admin(callback: CallbackQuery, state: FSMContext, bot:Bot):
    await state.clear()
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
        "Вы в режиме добавления позиций. Автоматически будет создан новый набор. Отправте в чат файл с позициями, которые хотите добавить, в таком формате"
    )
    await callback.message.answer(
        "Введите имя новой категории"
    )
    await state.set_state(File.waiting_for_name)

@router.message(File.waiting_for_name)
async def upload_file_admin(message: Message, state: FSMContext, bot: Bot):
    name = message.text
    await state.update_data(name = name)
    await state.set_state(File.waiting_for_file)
    await message.answer("Отправте боту файл")

@router.message(File.waiting_for_file)
async def upload_add_file_admin(message: Message, state: FSMContext, bot: Bot):
    try:
        file = await bot.get_file(message.document.file_id)
        data = await state.get_data()
        name = data.get("name", "New set")
        file_bytes = await bot.download_file(file.file_path)
        response = await put_report(message.from_user.id, file_bytes, name=name)
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
    finally:
        await state.clear()





#==============================================================================================================================================================================================
# Unit analysis
#==============================================================================================================================================================================================


@router.callback_query(F.data.startswith("analise_unit"))
async def analyse_unit_menu(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id, unit_id = callback.data.split("_")[2:]
        await callback.message.answer(
            "Меню аналитики текущей модели",
            reply_markup= await inline_keyboards.create_unit_edit_menu(set_id, unit_id)
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Не удалось загрузить аналитический интерфейс, извините", reply_markup= inline_keyboards.main)


def escape_md_v2(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

def format_unit_report(data: dict) -> str:
    get = lambda key: escape_md_v2(data.get(key))
    return f"""
📊 *Отчет по юнит\\-экономике*

*Название:* `{get('name')}`
*Пользователи:* `{get('users')}`
*Клиенты:* `{get('customers')}`
*AVP:* `{get('AVP')}`
*APC:* `{get('APC')}`
*TMS:* `{get('TMS')}`
*COGS:* `{get('COGS')}`
*COGS1s:* `{get('COGS1s')}`
*FC:* `{get('FC')}`

🔢 *Ключевые метрики:*
\\- C1 \\(конверсия\\): {get("C1")}
\\- ARPC \\(доход с клиента\\): {get("ARPC")}
\\- ARPU \\(доход с пользователя\\): {get("ARPU")}
\\- CPA \\(цена привлечения пользователя\\): {get("CPA")}
\\- CAC \\(цена привлечения клиента\\): {get("CAC")}

💰 *Доходность:*
\\- CLTV \\(пожизненная ценность клиента\\): {get("CLTV")}
\\- LTV \\(ценность клиента с учетом C1\\): {get("LTV")}
\\- ROI: {get("ROI")} \\%
\\- UCM \\(юнит\\-contrib\\-маржа\\): {get("UCM")}
\\- CCM \\(клиент\\-contrib\\-маржа\\): {get("CCM")}

📈 *Выручка и прибыль:*
\\- Revenue \\(выручка\\): {get("Revenue")}
\\- Gross Profit \\(валовая прибыль\\): {get("Gross_profit")}
\\- Margin \\(маржа\\): {get("Margin")}
\\- FC \\(постоянные издержки\\): {get("FC")}
\\- Profit \\(прибыль\\): {get("Profit")}

⚖️ *Окупаемость:*
\\- Требуется юнитов до BEP: {get("Required_units_to_BEP")}
\\- BEP \\(точка безубыточности\\): {get("BEP")}

📌 *Прибыльна ли модель:* {"✅ Да" if data.get("CCM", 0)>0 else "❌ Нет"}
""".strip()


def format_bep_report(data: dict) -> str:
    get = lambda key: escape_md_v2(data.get(key, "Undefined"))
    return f"""
📊 *Отчет о точке безубыточности*

💰 *Параметры модели экономики:*
*Название:* `{get('name')}`
*Пользователи:* `{get('users')}`
*Клиенты:* `{get('customers')}`
*AVP:* `{get('AVP')}`
*APC:* `{get('APC')}`
*TMS:* `{get('TMS')}`
*COGS:* `{get('COGS')}`
*COGS1s:* `{get('COGS1s')}`
*FC:* `{get('FC')}`


💰 *Параметры мат модели:*
\\- CCM \\(клиент\\-contrib\\-маржа\\): {get("CCM")}
\\- FC \\(постоянные издержки\\): {get("FC")}

⚖️ *Окупаемость:*
\\- Требуется юнитов до BEP: {get("Required_units_to_BEP")}
\\- BEP \\(точка безубыточности\\): {get("BEP")}

📌 *Прибыльна ли модель:* {"✅ Да" if data.get("CCM", 0)>0 else "❌ Нет"}
""".strip()

@router.callback_query(F.data.startswith("count_unit_economics_"))
async def count_unit_economics(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        print(callback.data.split("_")[2:])
        set_id, unit_id = callback.data.split("_")[3:]
        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=unit_id
        )
        if not analysis:
            raise ValueError("Error while generating report")

        await callback.message.answer(
            format_unit_report(analysis[0]),
            reply_markup = inline_keyboards.main,
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Извините, не удалось провести анализ модели", reply_markup= inline_keyboards.main)
    finally:
        await state.clear()
#==============================================================================================================================================================================================
# Count unit BEP
#==============================================================================================================================================================================================


@router.callback_query(F.data.startswith("count_unit_bep"))
async def count_unit_bep(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id, model_id = callback.data.split("_")[3:]
        await callback.answer()

        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=model_id
        )

        if not analysis:
            logging.error("Failed to get report")
            await callback.message.answer(
                "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
                reply_markup=inline_keyboards.main)
            await callback.answer()
            return
        analysis = analysis[0]

        if not analysis.get("Required_units_to_BEP") or analysis.get("UCM")<=0:
            await callback.message.answer(
                "К сожалению, данная модель убыточна",
            )
            await callback.message.answer(
                "Точка безубыточности недостижима",
            )
            await callback.message.answer(
                format_bep_report(analysis),
                reply_markup=inline_keyboards.main,
                parse_mode = "MarkdownV2"
            )
            await callback.answer()
            return

        image_bytes_list = await get_unit_bep.get_unit_bep(telegram_id=callback.from_user.id, unit_id=model_id)

        if not image_bytes_list:
            logging.error("Failed to get visual report images from API.")
            await callback.message.answer(
                "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
                reply_markup=inline_keyboards.main)
            await callback.answer()
            return
        
        first_photo = BufferedInputFile(image_bytes_list[0], filename="report_1.png")
        caption_text = "📊 Вот ваш визуальный отчёт о точке безубыточности! 📈"
        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=model_id
        )
        if not analysis:
            raise ValueError("Error while generating report")
        await callback.message.answer_photo(
            photo=first_photo,
            caption=caption_text
        )

        for ind, photo_bytes in enumerate(image_bytes_list[1:], start=2):
            if photo_bytes is None:
                continue
            photo_file = BufferedInputFile(photo_bytes, filename=f"report_{ind}.png")
            await callback.message.answer_photo(
                photo=photo_file
            )

        await callback.message.answer(
            format_bep_report(analysis[0]),
            reply_markup=inline_keyboards.main,
            parse_mode = "MarkdownV2"
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Извините, не удалось посчитать точку безубыточности", reply_markup= inline_keyboards.main)
    finally:
        await state.clear()

#==============================================================================================================================================================================================
# Generate unit report
#==============================================================================================================================================================================================

@router.callback_query(F.data.startswith("generate_report_unit"))
async def generate_unit_report(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id, model_id = callback.data.split("_")[3:]
        await callback.answer()

        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=model_id
        )

        if not analysis:
            logging.error("Failed to get report")
            await callback.message.answer(
                "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
                reply_markup=inline_keyboards.main)
            await callback.answer()
            return
        analysis = analysis[0]


        await callback.answer("Готовлю ваш отчёт...", show_alert=False)
        docs = await get_unit_exel.get_unit_exel(telegram_id=callback.from_user.id, unit_id=model_id)

        if not docs:
            await callback.message.answer("Извините, не удалось загрузить отчёт. Обратитесь в поддержку.")
            return

        await callback.message.answer(
            "Вот ваш отчёт!"
        )

        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=BufferedInputFile(docs.getvalue(), filename="report.xlsx"),
            reply_markup=inline_keyboards.main
        )
        await state.clear()


    except Exception as e:
        logging.error(e)
        await callback.message.answer("Извините, не удалось посчитать точку безубыточности", reply_markup= inline_keyboards.main)
    finally:
        await state.clear()


#===========================================================================================================================
# Unit Когортный анализ
#===========================================================================================================================

@router.callback_query(F.data.startswith("cohort_analisis_"))
async def start_cohort_analisis(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id, model_id = callback.data.split("_")[2:]
        await callback.answer()
        await state.set_state(Cohort.handle_unit)
        await state.update_data(set_id = set_id)
        await state.update_data(model_id = model_id)

        """
        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=model_id
        )
        if not analysis:
            logging.error("Failed to get report")
            await callback.message.answer(
                "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
                reply_markup=inline_keyboards.main)
            await callback.answer()
            return
        analysis = analysis[0]
        """
        await callback.message.answer("Введите процент сохранения аудитории (retention rate, %)")
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)


@router.message(Cohort.handle_unit)
async def continue_cohort_analisis(message:Message, state: FSMContext, bot:Bot):
    retention = message.text
    try:
        if not retention:
            raise ValueError("Invalid retention rate given")
        retention = float(retention)
        await state.update_data(retention = retention)
        await state.set_state(Cohort.retention_rate)
        await message.answer("Введите ожидаемый месячный прирост аудитории (audience growth rate, %)")

    except Exception as e:
        logging.exception(e)
        await message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)
        raise


@router.message(Cohort.retention_rate)
async def finish_cohort_analisis(message:Message, state: FSMContext, bot:Bot):
    growth = message.text
    try:
        if not growth:
            raise ValueError("Invalid retention rate given")
        growth = float(growth)
        data = await state.get_data()
        set_id = data.get("set_id")
        model_id = data.get("model_id")
        retention = data.get("retention")
        await state.clear()
        result = await update_model_cohort_data.update_model_cohort_data(
            telegram_id=message.from_user.id,
            set_id = set_id,
            model_id = model_id,
            retention = retention,
            growth = growth
        )
        if not result:
            raise Exception("Error while patching model")
        
        zip_buf = await get_unit_cohort(
            telegram_id= message.from_user.id,
            unit_id= model_id
        )
        if not zip_buf:
            raise Exception("Error while getting report from the server")
        zip_buf = io.BytesIO(zip_buf)
        with zipfile.ZipFile(zip_buf, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith(('.png', '.xlsx')): 
                    file_bytes = zip_ref.read(filename)
                    file_buf = io.BytesIO(file_bytes)
                    file_buf.seek(0)

                    document = BufferedInputFile(file_buf.read(), filename=filename)
                    await bot.send_document(chat_id=message.from_user.id, document=document)
        await message.answer("Ваш отчет готов!", reply_markup= inline_keyboards.main)

    except Exception as e:
        logging.exception(e)
        await message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)
        raise
    finally:
        await state.clear()


#==============================================================================================================================================================================================
# Set text analisis
#==============================================================================================================================================================================================


@router.callback_query(F.data.startswith("analise_set"))
async def analyse_set_menu_latest(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id = callback.data.split("_")[2]
        await callback.message.answer(
            "Меню аналитики текущего сета",
            reply_markup= await inline_keyboards.create_set_edit_menu(set_id)
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Не удалось загрузить аналитический интерфейс, извините", reply_markup= inline_keyboards.main)



def format_model_report(data: dict) -> str:
    get = lambda key: escape_md_v2(data.get(key))
    return f"""
📊 *Отчет по юнит\\-экономике*

*Название:* `{get('name')}`
*Пользователи:* `{get('users')}`
*Клиенты:* `{get('customers')}`
*AVP:* `{get('AVP')}`
*APC:* `{get('APC')}`
*TMS:* `{get('TMS')}`
*COGS:* `{get('COGS')}`
*COGS1s:* `{get('COGS1s')}`
*FC:* `{get('FC')}`

🔢 *Ключевые метрики:*
\\- C1 \\(конверсия\\): {get("C1")}
\\- ARPC \\(доход с клиента\\): {get("ARPC")}
\\- ARPU \\(доход с пользователя\\): {get("ARPU")}
\\- CPA \\(цена привлечения пользователя\\): {get("CPA")}
\\- CAC \\(цена привлечения клиента\\): {get("CAC")}

💰 *Доходность:*
\\- CLTV \\(пожизненная ценность клиента\\): {get("CLTV")}
\\- LTV \\(ценность клиента с учетом C1\\): {get("LTV")}
\\- ROI: {get("ROI")} \\%
\\- UCM \\(юнит\\-contrib\\-маржа\\): {get("UCM")}
\\- CCM \\(клиент\\-contrib\\-маржа\\): {get("CCM")}

📈 *Выручка и прибыль:*
\\- Revenue \\(выручка\\): {get("Revenue")}
\\- Gross Profit \\(валовая прибыль\\): {get("Gross_profit")}
\\- Margin \\(маржа\\): {get("Margin")}
\\- FC \\(постоянные издержки\\): {get("FC")}
\\- Profit \\(прибыль\\): {get("Profit")}

⚖️ *Окупаемость:*
\\- Требуется юнитов до BEP: {get("Required_units_to_BEP")}
\\- BEP \\(точка безубыточности\\): {get("BEP")}

📌 *Прибыльна ли модель:* {"✅ Да" if data.get("CCM", 0)>0 else "❌ Нет"}
""".strip()


def format_set_report(data:list):
    result = []
    for i, el in enumerate(data):
        buf = format_unit_report(el)
        if not buf:
            continue
        result.append(buf)
    return result


@router.callback_query(F.data.startswith("count_set_"))
async def count_set_economics(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        set_id = callback.data.split("_")[2]
        analysis = await get_set_report(
            telegram_id=callback.from_user.id,
            set_id = set_id
        )
        if not analysis:
            raise ValueError("Error while generating report")
        result = format_set_report(analysis)
        for i, el in enumerate(result):
            await callback.message.answer(
                el,
                parse_mode="MarkdownV2"
            )
        await callback.message.answer("Ваш отчет готов!", reply_markup = inline_keyboards.main)
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Извините, не удалось провести анализ модели", reply_markup= inline_keyboards.main)
    finally:
        await state.clear()


#===========================================================================================================================
# Сет визуализация
#===========================================================================================================================


@router.callback_query(F.data.startswith("visual_set"))
async def set_visualize_callback(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        set_id = int(callback.data.split("_")[2])
        await state.clear()
        zip_buf = await set_visualize(
            telegram_id= callback.from_user.id,
            set_id = set_id,
        )
        if not zip_buf:
            raise Exception("Error while getting report from the server")
        zip_buf = io.BytesIO(zip_buf)
        with zipfile.ZipFile(zip_buf, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith(('.png', '.xlsx')): 
                    file_bytes = zip_ref.read(filename)
                    file_buf = io.BytesIO(file_bytes)
                    file_buf.seek(0)

                    document = BufferedInputFile(file_buf.read(), filename=filename)
                    await bot.send_document(chat_id=callback.from_user.id, document=document)
        await callback.message.answer("Ваш отчет готов!", reply_markup= inline_keyboards.main)

    except Exception as e:
        logging.exception(e)
        await callback.message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)
        raise
    finally:
        await state.clear()

#===========================================================================================================================
# Сет XLSX отчет
#===========================================================================================================================

@router.callback_query(F.data.startswith("generate_report_set"))
async def set_generate_xlsx_report_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        set_id = int(callback.data.split("_")[3])
        await state.clear()

        xlsx_bytes = await set_generate_report(
            telegram_id=callback.from_user.id,
            set_id=set_id,
        )

        if not xlsx_bytes:
            raise Exception("Error while getting report from the server")

        file_buf = io.BytesIO(xlsx_bytes)
        file_buf.seek(0)

        document = BufferedInputFile(file_buf.read(), filename="report.xlsx")
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=document
        )

        await callback.message.answer("Ваш XLSX отчет готов!", reply_markup=inline_keyboards.main)

    except Exception as e:
        logging.exception(e)
        await callback.message.answer("Возникла ошибка при анализе", reply_markup=inline_keyboards.main)
        raise
    finally:
        await state.clear()

#===========================================================================================================================
# Сет когортный анализ
#===========================================================================================================================

@router.callback_query(F.data.startswith("cohort_set"))
async def start_set_cohort_analisis(callback: CallbackQuery, state: FSMContext, bot:Bot):
    try:
        await state.clear()
        set_id = int(callback.data.split("_")[2])
        await callback.answer()
        await state.set_state(SetCohort.handle_unit)
        await state.update_data(set_id = set_id)

        """
        analysis = await get_unit_report.get_unit_report(
            telegram_id=callback.from_user.id,
            unit_id=model_id
        )
        if not analysis:
            logging.error("Failed to get report")
            await callback.message.answer(
                "К сожалению, не удалось сгенерировать отчёт. Возможно, недостаточно данных 😔",
                reply_markup=inline_keyboards.main)
            await callback.answer()
            return
        analysis = analysis[0]
        """
        await callback.message.answer("Для коректности рузельтатов используется принцип ceteris paribus, параметры будут применены ко всем вложенным моделям")
        await callback.message.answer("Введите процент сохранения аудитории (retention rate, %)")
    except Exception as e:
        logging.error(e)
        await callback.message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)


@router.message(SetCohort.handle_unit)
async def continue_set_cohort_analisis(message:Message, state: FSMContext, bot:Bot):
    retention = message.text
    try:
        if not retention:
            raise ValueError("Invalid retention rate given")
        retention = float(retention)
        await state.update_data(retention = retention)
        await state.set_state(SetCohort.retention_rate)
        await message.answer("Введите ожидаемый месячный прирост аудитории (audience growth rate, %)")

    except Exception as e:
        logging.exception(e)
        await message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)
        raise


@router.message(SetCohort.retention_rate)
async def finish_set_cohort_analisis(message:Message, state: FSMContext, bot:Bot):
    growth = message.text
    try:
        if not growth:
            raise ValueError("Invalid retention rate given")
        growth = float(growth)
        data = await state.get_data()
        set_id = data.get("set_id")
        retention = data.get("retention")
        await state.clear()
        set_data = await retrieve_set(
            telegram_id= message.from_user.id,
            set_id= set_id
        )
        if not set_data:
            raise ValueError("No set data provided")
        models = set_data.get("units")
        if not models:
            raise ValueError("Error receiving models")
        for model in models:
            result = await update_model_cohort_data.update_model_cohort_data(
                telegram_id=message.from_user.id,
                set_id = set_id,
                model_id = model.get("id"),
                retention = retention,
                growth = growth
            )
            if not result:
                raise Exception("Error while patching model")

        zip_buf = await get_set_cohort(
            telegram_id= message.from_user.id,
            set_id=set_id
        )
        if not zip_buf:
            raise Exception("Error while getting report from the server")
        zip_buf = io.BytesIO(zip_buf)
        with zipfile.ZipFile(zip_buf, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith(('.png', '.xlsx')): 
                    file_bytes = zip_ref.read(filename)
                    file_buf = io.BytesIO(file_bytes)
                    file_buf.seek(0)

                    document = BufferedInputFile(file_buf.read(), filename=filename)
                    await bot.send_document(chat_id=message.from_user.id, document=document)
        await message.answer("Ваш отчет готов!", reply_markup= inline_keyboards.main)

    except Exception as e:
        logging.exception(e)
        await message.answer("Возникла ошибка при анализе", reply_markup= inline_keyboards.main)
        raise
    finally:
        await state.clear()

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
        await callback.message.answer("К сожалению, у этой позиции нет фотографий. 🖼️")
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
# Отлов неизвестных обработчиков
#===========================================================================================================================

@router.callback_query()
async def unknown_callback(callback: CallbackQuery):
    logging.info(f"UNHANDLED CALLBACK: {callback.data}")
    await callback.answer(f"⚠️ Это действие не распознано. Получено: {callback.data}", show_alert=True)