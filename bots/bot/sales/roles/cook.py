from aiogram import Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bots.bot.sales.storage import db_orm
from bots.bot.sales.storage.db_orm import User, Order
from bots.bot.sales.utillity.pages import page


class UserStates(StatesGroup):
    menu = State()

def get_emojy(order):
    return ["✅" if order.order_status == x else "❎" for x in ["cooking", "done", "issued"]]

async def welcome_handler(message: types.Message, state: FSMContext):
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    print(s.query(Order))
    if s.query(Order).first() is not None:
        for order in s.query(Order).all():
            if order.order_status != "issued":
                page_par = page.PageParser("storage/pages/cook.conf", *get_emojy(order), id=order.order_id, product=order.order)
                page_loaded = page_par.get_page()
                await message.answer(page_loaded.text, "HTML", reply_markup=page_loaded.inline_keyboard)



async def buttons(callback_query: types.CallbackQuery, state: FSMContext):
    name = callback_query.data.split("_")[2]
    print(name)
    print(callback_query.data)
    order_id = int(callback_query.data.split("_")[4])
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    order = s.query(db_orm.Order).where(db_orm.Order.order_id == order_id).first()
    if name == "cooking" or name == "done" or name == "issued":
        name_list = ["cooking", "done", "issued"]
        emojy_list = ["✅" if name == x else "❎" for x in name_list]
        order.order_status = name
        s.commit()
        page_par = page.PageParser("storage/pages/cook.conf", *emojy_list, id=order_id,
                                   product=order.order)
        page_loaded = page_par.get_page()
        print(page_loaded.text)
        await callback_query.message.edit_text(page_loaded.text, "HTML", reply_markup=page_loaded.inline_keyboard)

    if name == "delete":
        s.query(db_orm.Order).where(db_orm.Order.order_id == order_id).delete()
        s.commit()
        await callback_query.message.delete()


def register_handlers(dp: Dispatcher):
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    s.query(db_orm.User).filter(db_orm.User.user_id == 0).all()
    dp.message(welcome_handler, lambda id_user: len(s.query(db_orm.User).filter(db_orm.User.user_id == id_user.chat.id).all()) == 1,
                                commands="cook", state="*")
    dp.message(buttons, lambda c: c.data[:6] == 'button', state="*")
