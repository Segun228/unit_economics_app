from aiogram.fsm.state import StatesGroup, State


class Set(StatesGroup):
    handle_set = State()
    handle_edit_set = State()
    name = State()
    description = State()
    edit_description = State()
    set_id = State()

class Unit(StatesGroup):
    handle_unit = State()
    handle_edit_unit = State()
    model_set = State()
    name = State()
    users = State()
    customers = State()
    AVP = State()
    APC = State()
    TMS = State()
    COGS = State()
    COGS1s = State()
    FC = State()


class UnitEdit(StatesGroup):
    handle_unit = State()
    handle_edit_unit = State()
    model_set = State()
    name = State()
    users = State()
    customers = State()
    AVP = State()
    APC = State()
    TMS = State()
    COGS = State()
    COGS1s = State()
    FC = State()


class Send(StatesGroup):
    handle = State()
    message = State()


class File(StatesGroup):
    waiting_for_file = State()
    waiting_for_name = State()
    waiting_for_replace_file = State()


class Cohort(StatesGroup):
    handle_unit = State()
    retention_rate = State()
    audience_growth_rate = State()


class SetCohort(StatesGroup):
    handle_unit = State()
    retention_rate = State()
    audience_growth_rate = State()
