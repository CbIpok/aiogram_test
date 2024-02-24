from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import sessionmaker

from bots.bot.sales.storage import db_orm
from bots.bot.sales.storage.db_orm import User, Order


class UnknownStates(StatesGroup):
    name = State()
    number = State()


async def welcome_handler(message: types.Message, state: FSMContext):
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    if len(s.query(db_orm.User).filter(db_orm.User.user_id == message.chat.id).all()) == 0:
        await message.answer("welcome! enter name")
        await state.set_state(UnknownStates.name.state)
    else:
        await message.answer("you already registered")




async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer("enter number")
    await UnknownStates.next()


async def number_handler(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text.lower())
    await state.update_data(page_number=[1, 1, 1])
    async with state.proxy() as data:
        await message.answer(f"name:{data['name']} number: {data['number']}")
        session = sessionmaker(bind=db_orm.engine)
        s = session()
        user = User(name=data['name'], phone_number=data['number'], role="user")
        user.user_id = message.chat.id
        s.add(user)
        s.commit()
    await state.finish()


def register_handlers(dp: Dispatcher):
    global disp
    disp = dp
    dp.message(welcome_handler, commands="start", state="*")
    dp.message(name_handler, state=UnknownStates.name.state)
    dp.message(number_handler, state=UnknownStates.number.state)


