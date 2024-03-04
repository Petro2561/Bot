def encryption_mixin(text, key, is_encryption):
    key = int(key)
    final_string = ""
    for symbol in text:
        if symbol.isupper():
            symbol_index = ord(symbol) + ord("А")
            if is_encryption:
                symbol_position = (symbol_index + key) % 32 + ord("А")
            else:
                symbol_position = (symbol_index - key) % 32 + ord("А")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        elif symbol.islower():
            symbol_index = ord(symbol) - ord("а")
            if is_encryption:
                symbol_position = (symbol_index + key) % 32 + ord("а")
            else:
                symbol_position = (symbol_index - key) % 32 + ord("а")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        elif symbol.isdigit():
            # если это число, сдвиньте его фактическое значение
            if is_encryption:
                symbol_index = (int(symbol) + key) % 10
            else:
                symbol_index = (int(symbol) - key) % 10
            final_string += str(symbol_index)
        elif ord(symbol) >= 32 and ord(symbol) <= 47:
            # если это число,4 сдвинуть его фактическое значение
            symbol_index = ord(symbol) - ord(" ")
            if is_encryption:
                symbol_position = (symbol_index + key) % 15 + ord(" ")
            else:
                symbol_position = (symbol_index - key) % 15 + ord(" ")
            symbol_new = chr(symbol_position)
            final_string += symbol_new
        else:
            # если нет ни алфавита, ни числа, оставьте все как есть
            final_string += symbol
    return final_string
