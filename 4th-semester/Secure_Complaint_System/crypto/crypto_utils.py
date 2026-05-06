# crypto/crypto_utils.py

import secrets
import string
from typing import Tuple, Union

from Crypto.Cipher import AES
from Crypto.Hash import SHA256


BLOCK_SIZE = 16       # AES block size (bytes)
AES_KEY_SIZE = 32     # 256-bit keys


# ---------- basic helpers ----------

def _to_bytes(data: Union[str, bytes]) -> bytes:
    if isinstance(data, bytes):
        return data
    return data.encode("utf-8")


def hash_sha256(data: Union[str, bytes]) -> str:
    b = _to_bytes(data)
    h = SHA256.new()
    h.update(b)
    return h.hexdigest()


# ---------- PKCS#7 padding ----------

def pad_pkcs7(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    # Apply PKCS#7 padding to make len(data) a multiple of block_size.
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def unpad_pkcs7(padded: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    if not padded:
        raise ValueError("Invalid padding: empty data")

    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding length")

    if padded[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS#7 padding bytes")

    return padded[:-pad_len]


# ---------- AES-CBC encryption ----------

def generate_aes_key(length: int = AES_KEY_SIZE) -> bytes:
    return secrets.token_bytes(length)


def aes_encrypt_cbc(key: bytes, plaintext: Union[str, bytes]) -> Tuple[str, str]:
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")

    iv = secrets.token_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    pt_bytes = _to_bytes(plaintext)
    padded = pad_pkcs7(pt_bytes)
    ct = cipher.encrypt(padded)

    return iv.hex(), ct.hex()


def aes_decrypt_cbc(key: bytes, iv_hex: str, ciphertext_hex: str) -> str:
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")

    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ciphertext_hex)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = cipher.decrypt(ct)
    pt = unpad_pkcs7(padded)

    return pt.decode("utf-8", errors="ignore")


# ---------- password hashing & IDs ----------

def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
    if salt is None:
        salt_bytes = secrets.token_bytes(16)
        salt = salt_bytes.hex()
    else:
        # ensure salt is hex string
        bytes.fromhex(salt)  # will raise if invalid

    salted = (password + salt).encode("utf-8")
    h = SHA256.new()
    h.update(salted)
    return h.hexdigest(), salt


def generate_id(prefix: str = "id") -> str:
    return f"{prefix}_{secrets.token_hex(8)}"


def generate_secure_token(length: int = 32) -> str:
    return secrets.token_hex(length)


def generate_human_readable_id(prefix: str, length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    body = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}-{body}"
