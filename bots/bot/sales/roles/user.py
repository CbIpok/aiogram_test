import json
# from distutils.cmd import Command

from aiogram import Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, FSInputFile, InputMediaPhoto
from sqlalchemy.orm import sessionmaker

from bots.bot.sales.storage.keyboards.handlers import menu_choose, basket
from bots.bot.sales.storage.keyboards.handlers.menu_choose import busket_scroller
from bots.bot.sales.utillity.pages import page
from bots.bot.sales.storage import db_orm
from bots.bot.sales.utillity.pages.display import DisplayParser
from aiogram import F
from bots.bot.sales import storage

router = Router()


class UserStates(StatesGroup):
    menu = State()


# lambda id_user: check_user(sessionmaker(bind=db_orm.engine)()
@router.message((F.from_user.id == 536212157) & (F.text == '/menu'))
async def welcome_handler(message: types.Message, state: FSMContext):
    await message.answer("Menu:")
    await state.set_state(UserStates.menu.state)
    await page_handler(message, state)


def init_products():
    products = {}


async def page_handler(message: types.Message, state: FSMContext):
    await state.update_data(page_number=[1, 1, 1])
    data = await state.update_data(products={})
    session = sessionmaker(db_orm.engine)
    s = session()
    orders = s.query(db_orm.Display).all()
    for order_id in orders:
        order = s.query(db_orm.Page).where(db_orm.Page.page_id == order_id.page_id).first()
        # image = open(order.image_file_name, 'rb')
        keys = []
        for line in json.loads(open(order.inline_buttons_content_file_name).read().format(page_id=order_id.page_id)):
            buttons = [InlineKeyboardButton(text=name, callback_data=callback_name) for name, callback_name in line]
            keys.append(buttons)
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=keys)
        await message.answer_photo(FSInputFile(order.image_file_name), order.text, "HTML", reply_markup=inline_keyboard)
    # for page_info in display_parser.get_display():
    #     # async with state.proxy() as storage:
    #     #     page_obj = await render_page(storage, menu_number, 1)
    #
    #     image = open(page_info.image_filename, 'rb')
    #     await message.answer_photo(image, page_info.text, "HTML", reply_markup=page_info.inline_keyboard)
    #
    #     menu_number += 1


async def handle_page(menu_number, message, state):
    async with state.proxy() as data:
        page_number = int(data["page_number"][menu_number - 1])
    page_par = page.PageParser(f"storage/pages/menus/menu{menu_number}/page{page_number}.conf")
    page_loaded = page_par.get_page()
    image = open(page_loaded.image_filename, 'rb')
    await message.answer_photo(image, page_loaded.text, "HTML", reply_markup=page_loaded.inline_keyboard)

@router.message(Command('basket'))
async def basket_handler(message: types.Message, state: FSMContext):
    await message.answer("Your basket:")
    data = await state.get_data()

    id_page = 1
    for key, value in data["products"].items():
        if value != 0:
            basket_page = page.PageParser("storage/pages/basket.conf", product=key, var=value)
            page_loaded = basket_page.get_page()
            await  basket.render_basket_page(data, key)
            await message.answer(page_loaded.text + "Продукт: " + key + " Количество: " + str(value), "HTML",
                                     reply_markup=page_loaded.inline_keyboard)
            id_page += 1
    await message.answer("press to submit order", reply_markup=
    InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="submit", callback_data="button_submit")]]))



# todo splt into moduls like keyboard/handlers/basket.py
@router.callback_query(F.data.startswith("button_"))
async def buttons(callback_query: types.CallbackQuery, state: FSMContext):
    # todo 2
    name = callback_query.data.split("_")[1]
    keyboard = callback_query.data.split("_")[1]

    session = sessionmaker(db_orm.engine)
    s = session()
    if keyboard == "basket":
        await storage.keyboards.handlers.basket.buttons(callback_query, state)
    # todo 1
    #  Сделать продукт полностью хранящимся в бд.
    #  Сделать всего 1 универсальный шаблон под любое блюдо.
    #  Блюдо содержит список возможных добавок


    if name == 'plus' or name == 'minus':
        menu_number = int(callback_query.data.split("_")[2])
        # async with state.proxy() as storage:
        #     storage["page_number"][menu_number - 1] = storage["page_number"][menu_number - 1] + (
        #         1 if name == "plus" else -1)
        #     page_number = storage["page_number"][menu_number - 1]
        #     page_obj = await render_page(storage, menu_number, page_number)
        #     image = open(page_obj.image_filename, 'rb')
        #     await callback_query.message.edit_media(
        #         types.InputMedia(type='photo', media=image, caption=page_obj.text, parse_mode="HTML"),
        #         reply_markup=page_obj.inline_keyboard)
        await menu_choose.scrolling(callback_query, name, s)

    elif name == 'buy' or name == 'buy-undo':
        await busket_scroller(callback_query, name, s, state)

    elif name == 'submit':

        data = await state.get_data()
        order = db_orm.Order(user_id=callback_query.message.chat.id,
                                 order=json.dumps(data["products"]), order_status="unhandled")
        s.add(order)
        s.commit()
        await callback_query.message.answer(f"order {data['products']} done")
        await state.clear()


    elif name == "add":
        await change_keyboard(callback_query, state, "add")


    elif name == "cancel":
        await change_keyboard(callback_query, state, "chose")


async def change_keyboard(callback_query, state, keyboard):
    menu_number = int(callback_query.data.split("_")[2])
    data = await state.get_data()
    page_number = data["page_number"][menu_number - 1]
    page_obj = await render_page(data, menu_number, page_number, keyboard=keyboard)
    image = open(page_obj.image_filename, 'rb')
    await callback_query.message.edit_caption(caption=page_obj.text, reply_markup=page_obj.inline_keyboard)


async def render_page(data, menu_number, page_number, keyboard="chose"):
    if f"product_{page_number}_{menu_number}" not in data["products"]:
        data["products"][f"product_{page_number}_{menu_number}"] = 0
    page_par = page.PageParser(f"storage/pages/menus/menu{menu_number}/page{page_number}.conf",
                               var=data["products"][f"product_{page_number}_{menu_number}"],
                               page_id=menu_number, keyboard=keyboard,
                               product=f"product_{page_number}_{menu_number}",
                               menu_step=page_number)
    page_obj = page_par.get_page()
    return page_obj


def check_user(s, id_user):
    print(s.query(db_orm.User).filter(db_orm.User.user_id == id_user.chat.id).all())
    return len(s.query(db_orm.User).filter(db_orm.User.user_id == id_user.chat.id).all()) == 1


def register_handlers(dp: Dispatcher):
    session = sessionmaker(bind=db_orm.engine)
    s = session()
    dp.message(welcome_handler, lambda id_user: check_user(s, id_user), commands="menu3", state="*")
    dp.message(buttons, lambda c: c.data.split("_")[0] == 'button', state=UserStates.menu.state)
    dp.message(basket_handler, lambda id_user: check_user(s, id_user),
               commands="basket", state="*")
