import asyncio
import logging
import sys
from os import getenv
import time
from threading import Thread
# from task import Task, Scheduler
from datetime import date, datetime
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from threading import Thread
import pickle
import multiprocessing
from src.test_types import Server
from bots.bot.sales.roles.unknown import my_router
# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6618135740:AAHTlP0Xe0dS8pUCHzqknGyXBbm1-cXC2bU"

# All handlers should be attached to the Router (or Dispatcher)

# r = Router(name=__name__)
# dp = Dispatcher()
# dp.include_router(unknown.my_router)

# print(dp.sub_routers)

user_id = 536212157

bot_ = None

thread = None


def log(message):
    server.msgs.append(message)

# unknown

# @dp.message(CommandStart())
# async def message_handler(message: Message, state: FSMContext):
#     await unknown.welcome_handler(message, state)
#
# @dp.message(unknown.UnknownStates.name)
# async def name_handler(message: types.Message, state: FSMContext):
#     await unknown.name_handler(message, state)



async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    log(message)
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.py.send_message(chat_id=message.chat.id, ...)`
    # tasks['note1'].set_policy_sec('interval', 40)
    # tasks['note2'].set_policy_date(datetime(2024, 2, 21, 13, 50, 0))
    #
    # with open('aiogram_objs/Message', 'rb') as f:
    #     msg = pickle.load(f)
    # msgp = pickle.dumps(message)
    # msg = pickle.loads(msgp)
    log(await message.answer(f"Hello, {hbold(message.from_user.full_name)}!"))
    # print(*[msg.text for msg in msgs], sep="\n")


# @r.message(Command('jobs'))
async def command_handler(message: Message):
    log(message)
    # log(await send_msg(f"{Task.list_of_tasks()}"))
    await message.answer("123")

# @r.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        pass
        # Send a copy of the received message
        # await message.send_copy(chat_id=message.chat.id)
        # await tasks['note1'].process_note_ans(message.text)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def send_msg(msg):
    return await bot_.send_message(user_id, msg)


async def main(bot) -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # And the run events dispatching

    # scheduler.add_job(send_msg, 'interval', seconds=7, id='my_job_id')
    # scheduler.start()
    await dp.start_polling(bot)


def main_sync() -> None:
    global bot_
    if not bot_:
        bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        bot_ = bot
        # server = Server(main_sync, stop)
        asyncio.run(main(bot))


def run_tread():
    global thread
    thread = multiprocessing.Process(target=main_sync)
    thread.daemon = True
    thread.start()


def stop():
    # bot_.close()
    # asyncio.run(dp.stop_polling())
    # thread.terminate()
    server.msgs = []
    # Scheduler().scheduler.remove_all_jobs()


# tasks = dict(note1=Task("note1", send_msg), note2=Task("note2", send_msg))
server: Server = Server(main_sync, stop, [])

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
if __name__ == "__main__":
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.message(CommandStart(), command_start_handler)
    dp.include_router(my_router)
    asyncio.run(dp.start_polling(bot))
