import json

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bots.bot.sales.storage import db_orm
from bots.bot.sales.utillity.pages import page


async def render_basket_page(data, name):
    page_par = page.PageParser(f"storage/pages/basket.conf", product=name,
                               var=data["products"][name])
    page_obj = page_par.get_page()
    print(page_obj.inline_buttons_content)
    return page_obj

async def buttons(callback_query: types.CallbackQuery, state: FSMContext):
    name = callback_query.data.split("_")[2]
    print(callback_query.data)
    if name == 'buy' or name == 'buy-undo':
        page_number = int(callback_query.data.split("_")[4])
        async with state.proxy() as data:
            if f"product_{page_number}_{menu_number}" not in data["products"]:
                data["products"][f"product_{page_number}_{menu_number}"] = 0
            data["products"][f"product_{page_number}_{menu_number}"] = data["products"][
                                                                           f"product_{page_number}_{menu_number}"] + (
                                                                           1 if name == "buy" else -1)

        page_obj = await render_basket_page(data, f"product_{page_number}_{menu_number}")
        await callback_query.message.edit_text(
            page_obj.text.encode('utf-8'), parse_mode=ParseMode.HTML,
            reply_markup=page_obj.inline_keyboard)

    elif name == 'delete':
        menu_number = int(callback_query.data.split("_")[5])
        page_number = int(callback_query.data.split("_")[4])
        async with state.proxy() as data:
            data["products"][f"product_{page_number}_{menu_number}"] = 0
            await callback_query.message.delete()



