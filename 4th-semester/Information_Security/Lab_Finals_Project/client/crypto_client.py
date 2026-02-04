import json
from typing import Dict, Any

from crypto.crypto_utils import (
    aes_encrypt_cbc,
)


class ClientCrypto:

    def __init__(self, send_request_callable):
        self.send_request = send_request_callable


    def get_session_key(self) -> bytes:
        req = {"action": "request_session_key"}
        resp = self.send_request(req)

        if resp.get("status") != "ok":
            raise RuntimeError("KDC error: Failed to obtain session key")

        session_key_hex = resp.get("session_key_hex")
        return bytes.fromhex(session_key_hex)


    def encrypt_complaint(self, plaintext: str) -> Dict[str, str]:
        key = self.get_session_key()
        iv_hex, ct_hex = aes_encrypt_cbc(key, plaintext)
        return {"iv": iv_hex, "ciphertext": ct_hex}


    def encrypt_reply(self, plaintext: str) -> Dict[str, str]:
        key = self.get_session_key()
        iv_hex, ct_hex = aes_encrypt_cbc(key, plaintext)
        return {"iv": iv_hex, "ciphertext": ct_hex}
