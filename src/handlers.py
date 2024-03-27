import base64
import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from constants import (
    CHOOSE_CHIPHER,
    CHOOSE_MODE,
    CIPHER_FUNCTIONS_WITH_KEY,
    CIPHER_FUNCTIONS_WITHOUT_DECRYPT,
    CIPHER_FUNCTIONS_WITHOUT_KEY,
    INPUT_KEY,
    INPUT_TEXT,
    INTERNAL_ERROR,
    MISTAKE_OF_ENCRYPTION,
    MODES_OF_ENCRYPTION,
    NEW_START_PHRASE,
    SHIFR_INPUT_TEXT,
    START_PHRASE,
    VALIDATE_DICTIONARY,
    YOUR_CHOOSE_MODE,
)
from keybords import inline
from utils.exceptions import ValidationError



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()


@router.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(START_PHRASE)
    await message.answer(CHOOSE_CHIPHER, reply_markup=inline.keyboard_start)


async def text_input(message: types.Message, cipher: str, state: FSMContext) -> None:
    await message.reply(SHIFR_INPUT_TEXT)
    await state.update_data(cipher=cipher)
    await state.set_state("input_text")


@router.callback_query_handler(
    lambda cipher: cipher.data in CIPHER_FUNCTIONS_WITH_KEY
    or cipher.data in CIPHER_FUNCTIONS_WITHOUT_KEY
    or cipher.data in CIPHER_FUNCTIONS_WITHOUT_DECRYPT
)
async def choose_cipher(callback_query: types.CallbackQuery, state: FSMContext):
    cipher = callback_query.data
    await callback_query.message.answer(f"{YOUR_CHOOSE_MODE} {cipher}")
    if cipher in CIPHER_FUNCTIONS_WITHOUT_DECRYPT:
        await text_input(message=callback_query.message, cipher=cipher, state=state)
    else:
        await callback_query.message.reply(
            CHOOSE_MODE, reply_markup=inline.keyboard_choose_mode
        )
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
        logger.error(f"{MISTAKE_OF_ENCRYPTION} {error}")
        await state.finish()
        await message.answer(f"{error} {NEW_START_PHRASE}")


@router.callback_query_handler(lambda choice: choice.data in MODES_OF_ENCRYPTION)
async def choose_mode(callback_query: types.CallbackQuery, state: FSMContext):
    mode = callback_query.data
    data = await state.get_data()
    cipher = data.get("cipher")
    await state.update_data(mode=mode)
    await callback_query.message.answer(f"{YOUR_CHOOSE_MODE} {mode}")
    await callback_query.message.answer(INPUT_TEXT)
    if cipher in CIPHER_FUNCTIONS_WITH_KEY:
        await state.set_state("input_key")
    else:
        await state.set_state("input_text")
    await callback_query.message.edit_reply_markup(reply_markup=None)


@router.message_handler(state="input_key")
async def input_key(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state("input_text")
    await message.reply(INPUT_KEY)


@router.message_handler(state="input_text")
async def process_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cipher = data.get("cipher")
    mode = data.get("mode")
    if cipher in CIPHER_FUNCTIONS_WITH_KEY:
        text = data.get("text")
        key = message.text
    else:
        text = message.text 
    is_encryption = False if mode == "Дешифрование" else True
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
            VALIDATE_DICTIONARY.get(cipher)(
                text=text, key=key, is_encryption=is_encryption
            )
            result = CIPHER_FUNCTIONS_WITH_KEY.get(cipher).get(mode)(
                text=text, key=key, is_encryption=is_encryption
            )
            await process_cipher_result(message, result, state)
    except ValidationError as error:
        logger.error(f"{MISTAKE_OF_ENCRYPTION}: {error}")
        await state.finish()
        await message.answer(f"{error} {NEW_START_PHRASE}")
    except Exception as error:
        logger.error(f"{MISTAKE_OF_ENCRYPTION}: {error}")
        await state.finish()
        await message.answer(f"{INTERNAL_ERROR} {NEW_START_PHRASE}")
