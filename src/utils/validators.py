from utils.exceptions import ValidationError

list_value_caesar = [
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    " ",
    ".",
    ",",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "(",
    ")",
    "*",
    "+",
    "-",
    "/",
    "'",
    "~",
    "|",
    "}",
    "{",
    "[",
    "]",
    "=",
    "?",
    "_",
    "@",
    "<",
    ">",
]

list_value_morse = [
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    " ",
    ".",
    ",",
    "!",
    '"',
    "?",
    "$",
    "%",
    "&",
    "(",
    ")",
    "*",
    "+",
    "-",
    "/",
    "'",
    "_",
    ";",
    ":",
    "=",
    "@",
    "~",
    "|",
    "}",
    "{",
    "[",
    "]",
    "<",
    ">",
    "#",
    "%",
    "*",
]

list_key_vigenere = [
    "а",
    "б",
    "в",
    "г",
    "д",
    "е",
    "ж",
    "з",
    "и",
    "й",
    "к",
    "л",
    "м",
    "н",
    "о",
    "п",
    "р",
    "с",
    "т",
    "у",
    "ф",
    "х",
    "ц",
    "ч",
    "ш",
    "щ",
    "ъ",
    "ы",
    "ь",
    "э",
    "ю",
    "я",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def validate_caesar(text, key, is_encryption):
    """Валидация шифра Цезаря"""
    if len(text) > 2000:
        raise ValidationError("Слишком большой текст")
    for char in text:
        if char.lower() not in list_value_caesar:
            raise ValidationError(f"Вы ввели недопустимый символ {char} в тексте")
    if text == "":
        raise ValidationError("Вы не ввели ни одного символа.")
    if not key:
        raise ValidationError("Необходимо ввести ключ")
    if key.isdigit() is False:
        raise ValidationError(f"{key} должен быть числом.")
    if int(key) > 15:
        raise ValidationError("Слишком большой ключ")
    if key == "":
        raise ValidationError("Вы не ввели ни одного символа.")


def validate_morse(text, is_encryption):
    """Валидация кода Морзе"""
    if is_encryption:
        if len(text) > 2000:
            raise ValidationError("Слишком большой текст")
    else:
        if len(text) > 15000:
            raise ValidationError("Слишком большой текст")
    for letter in text:
        if letter not in list_value_morse:
            raise ValidationError("Вы ввели недопустимый символ. Наша машина подерживает только русские буквы.")

    if text == "":
        raise ValidationError("Вы не ввели ни одного символа.")


def validate_qr(text):
    """ "Валидация QR-кода."""
    if len(text) > 2000:
        raise ValidationError("Слишком большой текст")
    if text == "":
        raise ValidationError("Вы не ввели ни одного символа.")


def validate_vigenere(text, key, is_encryption):
    """ "Валидация шифра Виженера."""
    if is_encryption:
        if len(text) > 2000:
            raise ValidationError("Слишком большой текст")
    else:
        if len(text) > 15000:
            raise ValidationError("Слишком большой текст")
    if text == "":
        raise ValidationError("Вы не ввели ни одного символа.")
    if not key:
        raise ValidationError("Необходимо ввести ключ")
    if len(key) > 30:
        raise ValidationError("Слишком длинный ключ")
    for char in key:
        if char not in list_key_vigenere:
            raise ValidationError(f"Вы ввели недопустимый символ {char}")
    if key == "":
        raise ValidationError("Вы не ввели ни одного символа.")


def validate_aes(text, key, is_encryption):
    """ "Валидация шифра AES."""
    if is_encryption:
        if len(text) > 2000:
            raise ValidationError("Слишком большой текст")
    else:
        if len(text) > 15000:
            raise ValidationError("Слишком большой текст")
    if text == "":
        raise ValidationError("Вы не ввели ни одного символа.")
    if not key:
        raise ValidationError("Необходимо ввести ключ")
    if len(key) > 30:
        raise ValidationError("Слишком длинный ключ")
    if key == "":
        raise ValidationError("Вы не ввели ни одного символа.")
