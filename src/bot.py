import base64
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from constants import CIPHER_FUNCTIONS_WITH_KEY, CIPHER_FUNCTIONS_WITHOUT_DECRYPT, CIPHER_FUNCTIONS_WITHOUT_KEY, MISTAKE_OF_ENCRYPTION, NEW_START_PHRASE, SHIFR_INPUT_TEXT, START_PHRASE, VALIDATE_DICTIONARY
from config import config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=config.bot_token.get_secret_value())
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*["Цезарь", "Виженер", "QR-Code", "Азбука Морзе", "AES"])
    await message.reply(START_PHRASE)
    await message.answer("Выберите шифр:", reply_markup=keyboard)

async def text_input(message: types.Message, cipher: str, state: FSMContext) -> None:
    await message.reply(SHIFR_INPUT_TEXT)
    await state.update_data(cipher=cipher)
    await state.set_state("input_text")


@dp.message_handler(
    lambda message: message.text in CIPHER_FUNCTIONS_WITH_KEY
    or message.text in CIPHER_FUNCTIONS_WITHOUT_KEY
    or message.text in CIPHER_FUNCTIONS_WITHOUT_DECRYPT
)
async def choose_cipher(message: types.Message, state: FSMContext):
    cipher = message.text
    if cipher in CIPHER_FUNCTIONS_WITHOUT_DECRYPT:
        await text_input(message=message, cipher=cipher, state=state)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Шифрование", callback_data="encrypt"),
            InlineKeyboardButton("Дешифрование", callback_data="decrypt"),
        )
        await message.reply("Выберите режим:", reply_markup=keyboard)
        await types.ChatActions.typing()
        await state.update_data(cipher=cipher)


async def process_cipher_result(message: types.Message, result, state: FSMContext):
    try:
        data = await state.get_data()
        if data.get("cipher") == "QR-Code":
            photo_bytes = base64.b64decode(result)
            await message.reply_photo(photo_bytes)
        else:
            await message.reply(result)
        await state.finish()
        await message.answer(NEW_START_PHRASE)
    except Exception as error:
        logger.error(f"Error processing cipher: {error}")
        await state.finish()
        await message.answer(f"{error} {NEW_START_PHRASE}")


@dp.callback_query_handler(lambda c: c.data in ["encrypt", "decrypt"])
async def choose_mode(callback_query: types.CallbackQuery, state: FSMContext):
    mode = callback_query.data
    choice = "Шифрование" if mode == "encrypt" else "Дешифрование"
    await state.update_data(mode=mode)
    await callback_query.message.answer(f"Вы выбрали режим {choice}")
    await callback_query.message.answer("Введите текст для обработки:")
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await state.set_state("input_text")


@dp.message_handler(state="input_text")
async def process_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()
    cipher = data.get("cipher")
    mode = data.get("mode")
    is_encryption = False if mode == 'decrypt' else True
    
    try:
        if cipher in CIPHER_FUNCTIONS_WITHOUT_DECRYPT:
            VALIDATE_DICTIONARY.get(cipher)(text=text)
            result = CIPHER_FUNCTIONS_WITHOUT_DECRYPT.get(cipher)(text)
            await process_cipher_result(message, result, state)
        elif cipher in CIPHER_FUNCTIONS_WITHOUT_KEY:
            VALIDATE_DICTIONARY.get(cipher)(text, is_encryption=is_encryption)
            result = CIPHER_FUNCTIONS_WITHOUT_KEY.get(cipher).get(mode)(text)
            await process_cipher_result(message, result, state)
        else:
            await state.set_state("input_key")
            await message.reply("Введите ключ")
    except Exception as error:
        logger.error(f"{MISTAKE_OF_ENCRYPTION}: {error}")
        await state.finish()
        await message.answer(f"{error} {NEW_START_PHRASE}") 

@dp.message_handler(state="input_key")
async def input_key(message: types.Message, state: FSMContext):
    key = message.text
    data = await state.get_data()
    cipher = data.get("cipher")
    mode = data.get("mode")
    text = data.get("text")
    is_encryption = False if mode == 'decrypt' else True
    try:
        VALIDATE_DICTIONARY.get(cipher)(text=text, key=key, is_encryption=is_encryption)
        result = CIPHER_FUNCTIONS_WITH_KEY.get(cipher).get(mode)(text=text, key=key, is_encryption=is_encryption)
        await process_cipher_result(message, result, state)
    except Exception as error:
        logger.error(f"Error processing cipher: {error}")
        await state.finish()
        await message.answer(f"{error} {NEW_START_PHRASE}")

    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
