from aiogram import Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import sessionmaker
from aiogram.filters import CommandStart, Command
from bots.bot.sales.storage import db_orm
from bots.bot.sales.storage.db_orm import User, Order

# from bots.bot.sales.main import dp

my_router = Router()


class UnknownStates(StatesGroup):
    name = State()
    number = State()


@my_router.message(CommandStart())
async def welcome_handler(message: types.Message, state: FSMContext):
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    if len(s.query(db_orm.User).filter(db_orm.User.user_id == message.chat.id).all()) == 0:
        await message.answer("welcome! enter name")
        await state.set_state(UnknownStates.name.state)
    else:
        await message.answer("you already registered")


@my_router.message(UnknownStates.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer("enter number")
    await state.set_state(UnknownStates.number)

@my_router.message(UnknownStates.number)
async def number_handler(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text.lower())
    await state.update_data(page_number=[1, 1, 1])
    data = await state.get_data()
    await message.answer(f"name:{data['name']} number: {data['number']}")
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    user = User(name=data['name'], phone_number=data['number'], role="user")
    user.user_id = message.chat.id
    s.add(user)
    s.commit()
    await state.clear()


def register_handlers(dp: Dispatcher):
    pass
    # dp.include_router(my_router)
    # dp.message(welcome_handler, commands="start", state="*")
    # dp.message(name_handler, state=UnknownStates.name.state)
    # dp.message(number_handler, state=UnknownStates.number.state)
