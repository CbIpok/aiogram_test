import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


def get_calendar_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Calender",
            web_app=WebAppInfo(
                url="https://shitposting.su/",
            ),
        )
    )

    return builder.as_markup(
        is_persistent=True,
        resize_keyboard=True,
    )


@router.message(Command("start"))
async def enter_date(message: Message) -> None:
    await message.answer(
        text="Calendar",
        reply_markup=get_calendar_keyboard(),
    )


@router.message(F.web_app_data)
async def enter_date(message: Message) -> None:
    await message.answer("Test")


async def main():
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    await dispatcher.start_polling(
        Bot(token="6618135740:AAHTlP0Xe0dS8pUCHzqknGyXBbm1-cXC2bU"),
        allowed_updates=dispatcher.resolve_used_update_types(),
    )

asyncio.run(main())