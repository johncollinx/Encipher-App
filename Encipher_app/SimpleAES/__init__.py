from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes

from .tuples import *

# Setting #
MODE = AES.MODE_CBC
PADDING_STYLE = "pkcs7"
###########


def encrypt(data: bytes) -> EncryptResult:
    key = get_random_bytes(16)

    cipher = AES.new(
        key=key,
        mode=MODE
    )

    data = pad(
        data_to_pad=data,
        block_size=AES.block_size,
        style=PADDING_STYLE
    )

    data = cipher.encrypt(
        plaintext=data
    )

    return EncryptResult(
        key=key.hex(),
        iv=cipher.iv.hex(),
        data=data.hex()
    )


def decrypt(key: str, iv: hex, data: str) -> bytes:
    # hex -> bytes
    key = bytes.fromhex(key)
    iv = bytes.fromhex(iv)
    data = bytes.fromhex(data)

    cipher = AES.new(
        key=key,
        mode=MODE,
        iv=iv
    )

    data = cipher.decrypt(data)

    return unpad(
        padded_data=data,
        block_size=AES.block_size,
        style=PADDING_STYLE
    )
