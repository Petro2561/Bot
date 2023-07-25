import base64
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
# from encryption.utils import aes, caesar_code, morse_code, qr_code, vigenere
import aes, caesar_code, morse_code, qr_code, vigenere
from .validators import (validate_aes, validate_caesar,
                                   validate_morse, validate_qr,
                                   validate_vigenere)

logging.basicConfig(level=logging.INFO)


API_TOKEN = "6390553725:AAEAXrhGHklm4_EfYI3HL0tdKxIJjdzShdI"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


cipher_functions = {
    "Цезарь": {
        "encrypt": caesar_code.encryption_mixin,
        "decrypt": caesar_code.encryption_mixin,
    },
    "Азбука Морзе": {
        "encrypt": morse_code.encode,
        "decrypt": morse_code.decode
    },
    "QR-Code": qr_code.qr_code_generation,
    "Виженер": {"encrypt": vigenere.encode, "decrypt": vigenere.decode},
    "AES": {"encrypt": aes.encrypt, "decrypt": aes.decrypt},
}


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*["Цезарь", "Виженер", "QR-Code", "Азбука Морзе", "AES"])
    await message.reply("Я бот проекта Шифровальная машина")
    await message.answer("Выберите шифр:", reply_markup=keyboard)


# Обработчик выбора шифра
@dp.message_handler(
    lambda message: message.text
    in ["Цезарь", "Виженер", "QR-Code", "Азбука Морзе", "AES"]
)
async def choose_cipher(message: types.Message, state: FSMContext):
    cipher = message.text
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if cipher == "QR-Code":
        logging.basicConfig(level=logging.INFO)
        await message.reply("Введите текст для шифрования:")
        await state.update_data(cipher=cipher)
        await state.set_state("input_text")

    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Шифрование", callback_data="encrypt"),
            InlineKeyboardButton("Дешифрование", callback_data="decrypt"),
        )
        await message.reply("Выберите режим:", reply_markup=keyboard)
        await types.ChatActions.typing()

        # Сохранение выбранного шифра в состоянии пользователя
        await state.update_data(cipher=cipher)


# Обработчик нажатия на кнопку режима
@dp.callback_query_handler(lambda c: c.data in ["encrypt", "decrypt"])
async def choose_mode(callback_query: types.CallbackQuery, state: FSMContext):
    mode = callback_query.data
    choise = 'Шифрование' if mode == 'encypt' else 'Дешифрование'

    # Сохранение выбранного режима в состоянии пользователя
    await state.update_data(mode=mode)

    await callback_query.message.answer(f"Вы выбрали режим {choise}")
    await callback_query.message.answer("Введите текст для обработки:")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await state.set_state("input_text")


# Обработчик ввода текста
@dp.message_handler(state="input_text")
async def process_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)

    # Получение данных из состояния пользователя
    data = await state.get_data()
    cipher = data.get("cipher")
    mode = data.get("mode")
    if mode == "decrypt":
        is_encryption = False
    else:
        is_encryption = True

    if cipher == "QR-Code":
        try:
            validate_qr(text, key=None, is_encryption=is_encryption)
            cipher_function = cipher_functions.get(cipher)
            result = cipher_function(text)
            photo_bytes = base64.b64decode(result)
            await message.reply_photo(photo_bytes)
            await state.finish()
            await message.answer("Для нового шифрования нажмите /start")
        except Exception as error:
            await state.finish()
            await message.answer(
                f"Что-то пошло не так."
                f"{error} Для нового шифрования нажмите /start"
            )

    elif cipher == "Азбука Морзе":
        try:
            validate_morse(text, key=None, is_encryption=is_encryption)
            cipher_functions_dict = cipher_functions.get(cipher)
            cipher_function = cipher_functions_dict.get(mode)
            result = cipher_function(text)
            await message.reply(result)
            await state.finish()
            await message.answer("Для нового шифрования нажмите /start")
        except Exception as error:
            await state.finish()
            await message.answer(
                f"{error} Для нового шифрования нажмите /start"
            )
    else:
        await state.set_state("input_key")
        await message.reply("Введите ключ")


# Обработчик ввода ключа
@dp.message_handler(state="input_key", content_types=types.ContentTypes.TEXT)
async def input_key(message: types.Message, state: FSMContext):
    key = message.text

    # Получение данных из состояния пользователя
    data = await state.get_data()
    cipher = data.get("cipher")
    mode = data.get("mode")
    text = data.get("text")
    if data.get("mode") == "encrypt":
        is_encryption = True
    else:
        is_encryption = False

    # Получение функции шифрования или дешифрования
    # из словаря и вызов функции с текстом и ключом

    if cipher == "Цезарь":
        try:
            validate_caesar(text=text, key=key, is_encryption=is_encryption)
            cipher_functions_dict = cipher_functions.get(cipher)
            cipher_function = cipher_functions_dict.get(mode)
            key = int(key)
            result = cipher_function(text, key, is_encryption)
            await message.reply(result)
            await state.finish()
            await message.answer("Для нового шифрования нажмите /start")
        except Exception as error:
            await state.finish()
            await message.answer(
                f"{error} Для нового шифрования нажмите /start"
            )
    else:
        try:
            if cipher == 'AES':
                validate_aes(text=text, key=key, is_encryption=is_encryption)
            if cipher == 'Виженер':
                validate_vigenere(
                    text=text, key=key,
                    is_encryption=is_encryption
                )
            cipher_functions_dict = cipher_functions.get(cipher)
            cipher_function = cipher_functions_dict.get(mode)
            result = cipher_function(text, key)
            await message.reply(result)
            await state.finish()
            await message.answer("Для нового шифрования нажмите /start")
        except Exception as error:
            await state.finish()
            await message.answer(
                f"{error} Для нового шифрования нажмите /start"
            )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)