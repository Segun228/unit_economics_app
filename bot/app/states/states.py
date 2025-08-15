from aiogram.fsm.state import StatesGroup, State


class Category(StatesGroup):
    handle_category = State()
    handle_edit_category = State()
    name = State()
    description = State()
    category_id = State()

class Post(StatesGroup):
    handle_post = State()
    handle_edit_post = State()
    category = State()
    description = State()
    title = State()
    price = State()
    quantity = State()
    post_id = State()
    waiting_for_photos = State()


class Send(StatesGroup):
    handle = State()
    message = State()