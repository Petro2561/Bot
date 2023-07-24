import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def encrypt(text, key):
    text = text.encode("utf-8")
    key = key.encode("utf-8")
    key = SHA256.new(key).digest()
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    padding = AES.block_size - len(text) % AES.block_size
    text += bytes([padding]) * padding
    data = iv + encryptor.encrypt(text)
    return base64.b64encode(data).decode("latin-1")


def decrypt(text, key):
    key = key.encode("utf-8")
    text = base64.b64decode(text.encode("latin-1"))
    key = SHA256.new(key).digest()
    iv = text[: AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    data = decryptor.decrypt(text[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding].decode("utf-8")
