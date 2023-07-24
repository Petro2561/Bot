"""
Выбрана эта библиотека, как самая популярная
https://pypi.org/project/qrcode/
"""
import base64
from io import BytesIO

import qrcode


def qr_code_generation(text: str) -> str:
    # Создание QR-кода на основе заданного текста
    img = qrcode.make(text)
    # Создание буфера для сохранения изображения
    buffered = BytesIO()
    # Сохранение изображения в буфер
    img.save(buffered)
    # Преобразование изображения в строку base64
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


"""
При переходе по qr коду у пользователя открывается страница браузера, далее:
1)если зашифрована url, то открывается страница
2)если текст, то происходит запрос по этому тексту в поисковике
"""
