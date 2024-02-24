import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.orm import sessionmaker
from storage import db_orm
from storage.db_orm import Page, Display
from roles import unknown, user, cook
from aiogram.filters import CommandStart, Command
def load_token():
    return open("token.txt", "r").read()
user_id = 536212157
bot = Bot(token=load_token())
dp = Dispatcher(storage=MemoryStorage())
# asyncio.run(bot.send_message(user_id, "123"))


def create_menus():
    session = sessionmaker(db_orm.engine)
    s = session()
    for _ in range(1,4):
        p = Page()
        p.page_id = _
        p.text = f"shava{_}" + ' count:{product_count}'
        p.image_file_name = f"storage/images/{_}.jpg"
        p.inline_buttons_content_file_name = f"storage/keyboards/menu_chose.conf"
        p.catigory = "shava"
        s.add(p)
        s.commit()
    for _ in range(1,4):
        p = Page()
        p.page_id = _+3
        p.text = f"eda{_}" + ' count:{product_count}'
        p.image_file_name = f"storage/images/{_}.jpg"
        p.inline_buttons_content_file_name = f"storage/keyboards/menu_chose.conf"
        p.catigory = "eda"
        s.add(p)
        s.commit()
    for _ in range(1,4):
        p = Page()
        p.page_id = _+6
        p.text = f"voda{_}" + ' count:{product_count}'
        p.image_file_name = f"storage/images/{_}.jpg"
        p.inline_buttons_content_file_name = f"storage/keyboards/menu_chose.conf"
        p.catigory = "voda"
        s.add(p)
        s.commit()

def create_display():
    session = sessionmaker(db_orm.engine)
    s = session()
    for _ in range(0, 3):
        p = Display()
        p.page_id=_*3 + 1
        p.menu_id=_ + 1
        s.add(p)
        s.commit()

async def main():
    # db_orm.init_base()


    # create_menus()
    # create_display()
    unknown.register_handlers(dp)
    user.register_handlers(dp)
    cook.register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    print("1234")
    asyncio.run(main())

@dp.message(CommandStart())
async def save_vasya(query: types.CallbackQuery, state: FSMContext):
    print(123)
    global disp
    handlers = disp.callback_query_handlers.handlers
    await state.finish()
    for h in handlers:
        for f in h.filters:
            if f.filter(query):
                await h.handler(query)
                return