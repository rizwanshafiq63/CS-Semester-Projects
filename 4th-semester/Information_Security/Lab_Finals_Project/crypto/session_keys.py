import secrets
from Crypto.Hash import SHA256

from .crypto_utils import generate_aes_key


class SessionKeyManager:

    @staticmethod
    def generate_session_key() -> bytes:
        return generate_aes_key()


class EphemeralDH:

    P = 0xE95E4A5F737059DC60DFC7AD95B3D8139515620F
    G = 5

    def __init__(self):
        self.private = secrets.randbits(128)
        self.public = pow(self.G, self.private, self.P)
        self.session_key = None

    def compute_shared(self, peer_public: int) -> bytes:
        shared = pow(peer_public, self.private, self.P)
        shared_bytes = shared.to_bytes((shared.bit_length() + 7) // 8, "big")

        self.session_key = SHA256.new(shared_bytes).digest()
        return self.session_key

    def destroy(self):
        self.private = 0
        self.public = 0
        self.session_key = None
