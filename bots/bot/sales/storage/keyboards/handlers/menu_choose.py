import json

from aiogram import types
from storage import db_orm


async def scrolling(callback_query, name, s):
    page_id = int(callback_query.data.split("_")[2])
    page_id = page_id + (1 if name == "plus" else -1)
    order = s.query(db_orm.Page).where(db_orm.Page.page_id == page_id).first()
    image = open(order.image_file_name, 'rb')
    inline_keyboard = types.inline_keyboard.InlineKeyboardMarkup()
    for line in json.loads(open(order.inline_buttons_content_file_name).read().format(page_id=page_id)):
        buttons = [types.InlineKeyboardButton(name, callback_data=callback_name) for name, callback_name in line]
        inline_keyboard.add(*buttons)
    await callback_query.message.edit_media(
        types.InputMedia(type='photo', media=image, caption=order.text, parse_mode="HTML"),
        reply_markup=inline_keyboard)

async def busket_scroller(callback_query, name, s, state):
    page_id = int(callback_query.data.split("_")[2])
    async with state.proxy() as data:
        if f"product_{page_id}" not in data["products"]:
            data["products"][f"product_{page_id}"] = 0
        data["products"][f"product_{page_id}"] = data["products"][f"product_{page_id}"] + (
            1 if name == "buy" else -1)

        order = s.query(db_orm.Page).where(db_orm.Page.page_id == page_id).first()
        image = open(order.image_file_name, 'rb')
        inline_keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        for line in json.loads(open(order.inline_buttons_content_file_name).read().format(page_id=page_id)):
            buttons = [types.InlineKeyboardButton(name, callback_data=callback_name) for name, callback_name in line]
            inline_keyboard.add(*buttons)
        await callback_query.message.edit_media(
            types.InputMedia(type='photo', media=image,
                             caption=order.text.format(product_count=data["products"][f"product_{page_id}"]),
                             parse_mode="HTML"),
            reply_markup=inline_keyboard)