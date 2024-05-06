from collections import namedtuple as _namedtuple


EncryptResult = _namedtuple(
    "EncryptResult",
    "key iv data"
)
