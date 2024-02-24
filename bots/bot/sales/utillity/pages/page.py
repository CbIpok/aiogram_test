from aiogram import types

import json
import configparser
import io
from aiogram.types import InlineKeyboardMarkup


class Page:
    inline_keyboard: InlineKeyboardMarkup

    def __init__(self):
        self.text = ""
        self.image_filename = ""
        self.inline_keyboard = types.InlineKeyboardMarkup()
        self.inline_buttons_content = None


class PageGenerator(Page):

    def set_text(self, text: str):
        self.text = text

    def set_image_filename(self, image_filename: str):
        self.image_filename = image_filename

    def set_inline_keyboard(self, inline_keyboard: InlineKeyboardMarkup, inline_buttons_content: [[str, str]]):
        self.inline_keyboard = inline_keyboard
        self.inline_buttons_content = inline_buttons_content

    def save(self, file_name: str):
        config = configparser.ConfigParser()

        config["page"] = {
            "text": self.text,
            "image_filename": self.image_filename,
            "inline_buttons_content": "storage/keyboards/menu_{keyboard}.conf"
        }

        with open(file_name, 'w') as configfile:
            config.write(configfile)


class KeyboardGenerator:
    def __init__(self):
        self.inline_buttons_content = [[]]
        self.inline_keyboard = InlineKeyboardMarkup([[]])
        self.index = 0
    def init_keyboard(self):
        self.inline_keyboard = InlineKeyboardMarkup([[]])

    def add_button(self, text: str, callback: str):
        # self.inline_keyboard.add(types.InlineKeyboardButton(text, callback_data=callback))
        self.inline_buttons_content[self.index].append([text, callback])

    def end_line(self):
        self.index += 1
        self.inline_buttons_content.append([])

    def get_keyboard(self) -> [types.InlineKeyboardMarkup, [[str, str]]]:
        self._render()
        return [self.inline_keyboard, self.inline_buttons_content]

    def save(self,file_name: str):
        with open(file_name, 'w') as configfile:
            configfile.write(json.dumps(self.inline_buttons_content))

    def _render(self):
        for line in self.inline_buttons_content:
            buttons = [types.InlineKeyboardButton(text, callback_data=callback) for text, callback in line]
            self.inline_keyboard.add(*buttons)




class PageParser(Page):
    def __init__(self, page_filename, *args, **kwargs):
        super().__init__()
        config = configparser.ConfigParser()
        config_template = open(page_filename, "r").read()
        config_str = config_template.format(*args, **kwargs)
        config.read_string(config_str)


        page = config["page"]
        self.text = page["text"]
        self.image_filename = page["image_filename"]

        self.inline_buttons_content = json.loads(open(config.get("page", "inline_buttons_content"), "r").read().format(*args, **kwargs))
        inline_keyboard = types.inline_keyboard.InlineKeyboardMarkup()
        for line in self.inline_buttons_content:
            buttons = [types.InlineKeyboardButton(name, callback_data=callback_name) for name, callback_name in line]
            inline_keyboard.add(*buttons)
        self.inline_keyboard = inline_keyboard

    def get_page(self) -> Page:
        return self
