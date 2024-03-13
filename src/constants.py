from utils import aes, caesar_code, morse_code, qr_code, vigenere
from utils.validators import (
    validate_aes,
    validate_caesar,
    validate_morse,
    validate_qr,
    validate_vigenere,
)

START_PHRASE = "Я бот проекта Шифровальная машина"
SHIFR_INPUT_TEXT = "Введите текст для шифрования:"
NEW_START_PHRASE = "Для нового шифрования нажмите /start"
MISTAKE_OF_ENCRYPTION = "Ошибка шифрования"
MODES_OF_ENCRYPTION = ["Шифрование", "Дешифрование"]
CIPHER_FUNCTIONS_WITH_KEY = {
    "Цезарь": {
        "Шифрование": caesar_code.encryption_mixin,
        "Дешифрование": caesar_code.encryption_mixin,
    },
    "Виженер": {"Шифрование": vigenere.encode, "Дешифрование": vigenere.decode},
    "AES": {"Шифрование": aes.encrypt, "Дешифрование": aes.decrypt},
}

CIPHER_FUNCTIONS_WITHOUT_KEY = {
    "Азбука Морзе": {"Шифрование": morse_code.encode, "Дешифрование": morse_code.decode}
}
CIPHER_FUNCTIONS_WITHOUT_DECRYPT = {"QR-Code": qr_code.qr_code_generation}

VALIDATE_DICTIONARY = {
    "Цезарь": validate_caesar,
    "Виженер": validate_vigenere,
    "AES": validate_aes,
    "Азбука Морзе": validate_morse,
    "QR-Code": validate_qr,
}
