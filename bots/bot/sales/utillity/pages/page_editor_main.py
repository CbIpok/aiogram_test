import page
from utillity.pages.display import DisplayGenerator, DisplayParser

def gen_display():
    display_gen = DisplayGenerator()
    for menu_number in range(1,4):
        display_gen.add_page_as_file(f"../../data/pages/menus/menu{menu_number}/page1.conf")
    display_gen.save("display.conf")
def gen_page(page_number: int,menu_number: int):
    page_gen = page.PageGenerator()
    token = '{var}'
    page_gen.set_text(f"""<b>Блюдо HTML Images {page_number}-{menu_number}</b>
        <strong>bold {token} </strong>""")

    page_gen.set_image_filename(f"data/images/{page_number}.jpg")

    keyboard_generator = page.KeyboardGenerator()
    keyboard_generator.init_keyboard()
    keyboard_generator.add_button("<", f"button_minus_{menu_number}")
    keyboard_generator.add_button(">", f"button_plus_{menu_number}")
    keyboard_generator.end_line()
    keyboard_generator.add_button("+", f"button_buy_{menu_number}")
    keyboard_generator.add_button("-", f"button_buy-undo_{menu_number}")
    keyboard_generator.add_button("add", f"button_add_{menu_number}")
    keyboard, inline_buttons_content = keyboard_generator.get_keyboard()
    page_gen.set_inline_keyboard(keyboard, inline_buttons_content)

    page_gen.save(f"../../data/pages/menus/menu{menu_number}/page{page_number}.conf")

def parse_conf(page_number: int,menu_number: int):
    page_par = page.PageParser(f"../../data/pages/menus/menu{menu_number}/page{page_number}.conf")
    return page_par.get_page().text, page_par.get_page().image_filename, page_par.get_page().inline_keyboard

def main():
    for menu_number in range(1, 4):
        for page_number in range(1, 4):
            gen_page(page_number, menu_number)

    gen_display()

if __name__ == "__main__":
    main()
