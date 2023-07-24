NOT_DEFINED_LANG = "nd"


def vigenere_codec(text: str, key: str, codec: int = 1):
    """
    Код Виженера.
    Для повышения устойчивости все слова переводятся в верхний регистр,
    Цифры и знаки не шифруются. Исходный текст желательно вводить без пробелов.
    В фунцию передается текст для шифровки/дешифровки,
    ключ шифрования,
    опционально: параметр codec для определения
    направления шифрования (1 - шифровка(умолч.)/ -1 - дешифровка),
    """

    result = ""
    key = key.upper()
    # Словарь алфавитов.
    # название_языка : [код_первого_символа, длина_алфавита]
    lang_dict = {"en": [64, 26], "ru": [1039, 32]}

    # Определяем язык ключа. Язык по умолчанию NOT_DEFINED_LANG
    lang = NOT_DEFINED_LANG
    for letter in key:
        for lang_test, [lang_start, lang_len] in lang_dict.items():
            if 0 <= (ord(letter) - lang_start) <= lang_len:
                lang = lang_test
                break
        if lang != NOT_DEFINED_LANG:
            break

    # Если язык неизвестен, то текст возвращается в исходном виде.
    if lang == NOT_DEFINED_LANG:
        return text

    # код первой буквы алфавита
    zero_letter = lang_dict[lang][0]
    # длина алфавита
    alphabet_length = lang_dict[lang][1]

    # Очищаем ключ от символов, не принадлежащих алфавиту
    new_key = ""
    for letter in key:
        if zero_letter < ord(letter) < zero_letter + alphabet_length:
            new_key += letter

    # Шифрование предполагает сдвиг кода буквы на число,
    # соответствующее коду соответствующей буквы ключа.
    i = 0
    for letter in text.upper():
        if zero_letter < ord(letter) < zero_letter + alphabet_length:
            result += chr(
                (ord(new_key[i]) * codec - 1 + ord(letter) - 2 * zero_letter)
                % alphabet_length
                + zero_letter
            )
            i = i + 1 if i < len(new_key) - 1 else 0
        else:
            result += letter
    return result


def encode(text: str, key: str):
    return vigenere_codec(text, key, 1)


def decode(text: str, key: str):
    return vigenere_codec(text, key, -1)
