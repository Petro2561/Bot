from aiogram import types

keyboard_start = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(text="Цезарь", callback_data="Цезарь"),
    types.InlineKeyboardButton(text="Виженер", callback_data="Виженер"),
    types.InlineKeyboardButton(text="QR-Code", callback_data="QR-Code"),
    types.InlineKeyboardButton(text="Азбука Морзе", callback_data="Азбука Морзе"),
    types.InlineKeyboardButton(text="AES", callback_data="AES"),
]
for button in buttons:
    keyboard_start.row(button)


keyboard_choose_mode = types.InlineKeyboardMarkup(row_width=2)
keyboard_choose_mode.add(
    types.InlineKeyboardButton("Шифрование", callback_data="Шифрование"),
    types.InlineKeyboardButton("Дешифрование", callback_data="Дешифрование"),
)
