
from bots.bot.sales.utillity.pages.page import PageGenerator, Page, PageParser, KeyboardGenerator
import configparser
import json


# todo test DisplayParser by main


class DisplayGenerator:
    def __init__(self):
        self.display = []

    def add_page_as_file(self, file_name: str):
        self.display.append(file_name)

    def save(self, file_name: str):
        config = configparser.ConfigParser()
        config["display"] = {
            "page_count": len(self.display)
        }
        for i in range(len(self.display)):
            config["display"][f"page{i + 1}"] = f"data/pages/menus/menu1/page{i + 1}.conf"

        with open(file_name, 'w') as configfile:
            config.write(configfile)


class DisplayParser:
    def __init__(self, file_name: str):
        self.display = []
        config = configparser.ConfigParser()
        config.read(file_name)
        display_head = config["display"]
        for page_number in range(1, int(display_head["page_count"]) + 1):
            page_filename = display_head[f"page{page_number}"]
            page_parser = PageParser(page_filename, var=0, page_id=page_number, keyboard="chose")
            self.display.append(page_parser.get_page())

    def get_display(self) -> [Page]:
        return self.display
