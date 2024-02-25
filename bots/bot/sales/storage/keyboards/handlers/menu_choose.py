import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, FSInputFile
from bots.bot.sales.storage import db_orm


async def scrolling(callback_query, name, s):
    page_id = int(callback_query.data.split("_")[2])
    page_id = page_id + (1 if name == "plus" else -1)
    print(page_id)
    order = s.query(db_orm.Page).where(db_orm.Page.page_id == page_id).first()
    image = open(order.image_file_name, 'rb')
    inline_keyboard = []
    for line in json.loads(open(order.inline_buttons_content_file_name).read().format(page_id=page_id)):
        buttons = [types.InlineKeyboardButton(text=name, callback_data=callback_name) for name, callback_name in line]
        inline_keyboard.append(buttons)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await callback_query.message.edit_media(media=InputMediaPhoto(
            media=FSInputFile(order.image_file_name),
            caption=order.text
        ),
        reply_markup=inline_keyboard)

async def busket_scroller(callback_query, name, s, state):
    page_id = int((int(callback_query.data.split("_")[2]) - 1) / 3) + 1
    menu_id = int((int(callback_query.data.split("_")[2]) - 1) % 3) + 1
    data = await state.get_data()
    if f"product_{page_id}_{menu_id}" not in data["products"]:
        data["products"][f"product_{page_id}_{menu_id}"] = {'count': 0, 'adds': []}
    data["products"][f"product_{page_id}_{menu_id}"]["count"] = data["products"][f"product_{page_id}_{menu_id}"]["count"] = data["products"][f"product_{page_id}_{menu_id}"]["count"] + 1
    state.set_data(data=data)
    order = s.query(db_orm.Page).where(db_orm.Page.page_id == page_id).first()
    # image = open(order.image_file_name, 'rb')
    inline_keyboard = []
    for line in json.loads(open(order.inline_buttons_content_file_name).read().format(page_id=page_id)):
        buttons = [types.InlineKeyboardButton(text=name, callback_data=callback_name) for name, callback_name in line]
        inline_keyboard.append(buttons)
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await callback_query.message.edit_caption(caption=order.text.format(product_count=
                                                                            data["products"][f"product_{page_id}_{menu_id}"]["count"]),
                                                  reply_markup=inline_keyboard)
