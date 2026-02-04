# server/key_manager.py

import time
from typing import Dict, Any

from crypto.crypto_utils import (
    hash_password,
    generate_aes_key,
    generate_id,
)
from crypto.session_keys import SessionKeyManager 
from server.logger import Logger
from server.storage import (
    USER_FILE,
    SecureStorage
)


class KeyManager:
    def __init__(self, storage: SecureStorage):
        self.storage = storage

        # username -> user_record
        self.users: Dict[str, Dict[str, Any]] = self.storage.load_encrypted(USER_FILE)
        if not isinstance(self.users, dict):
            self.users = {}

        Logger.info("User store loaded")

    # User Registration

    def register_user(self, username: str, password: str, role: str) -> Dict[str, Any]:
        username = username.lower().strip()

        if username in self.users:
            Logger.warning(f"Registration failed — username exists: {username}")
            return {"status": "error", "message": "Username already exists"}

        if role not in ("user", "admin"):
            role = "user"

        pw_hash, salt = hash_password(password)

        long_term_key = generate_aes_key()
        key_id = generate_id("UKEY")

        user_record = {
            "username": username,
            "password_hash": pw_hash,
            "salt": salt,
            "role": role,
            "status": "active",
            "key_id": key_id,
            "long_term_key": long_term_key.hex(),
            "created_at": time.time(),
        }

        self.users[username] = user_record
        self._save_users()

        Logger.security(f"Registered user '{username}' with key_id={key_id}")
        return {"status": "ok", "message": "User registered successfully"}

    # Login

    def login(self, username: str, password: str) -> Dict[str, Any]:
        username = username.lower().strip()
        user = self.users.get(username)
        if not user:
            Logger.warning(f"Login failed — user not found: {username}")
            return {"status": "error", "message": "Invalid username or password"}

        pw_hash_attempt, _ = hash_password(password, salt=user["salt"])
        if pw_hash_attempt != user["password_hash"]:
            Logger.warning(f"Login failed — wrong password for: {username}")
            return {"status": "error", "message": "Invalid username or password"}

        if user["status"] != "active":
            Logger.warning(f"Login failed — user revoked: {username}")
            return {"status": "error", "message": "User account is revoked"}

        Logger.success(f"User logged in: {username}")
        return {"status": "ok", "username": username, "role": user["role"]}

    # KDC — Session Key (if needed)

    def issue_session_key(self) -> Dict[str, Any]:
        key = SessionKeyManager.generate_session_key()
        Logger.security("Issued new ephemeral session key")
        return {"status": "ok", "session_key_hex": key.hex()}

    # Key Rotation & Revocation

    def rotate_user_key(self, username: str) -> Dict[str, Any]:
        username = username.lower().strip()
        user = self.users.get(username)
        if not user:
            Logger.warning(f"Key rotation failed — user not found: {username}")
            return {"status": "error", "message": "User not found"}

        new_key = generate_aes_key()
        new_key_id = generate_id("UKEY")

        user["long_term_key"] = new_key.hex()
        user["key_id"] = new_key_id
        user["created_at"] = time.time()

        self._save_users()
        Logger.security(f"Rotated key for {username} → new key_id={new_key_id}")
        return {"status": "ok", "message": "User key rotated successfully"}

    def revoke_user(self, username: str) -> Dict[str, Any]:
        username = username.lower().strip()
        user = self.users.get(username)
        if not user:
            Logger.warning(f"Revocation failed — user not found: {username}")
            return {"status": "error", "message": "User not found"}

        user["status"] = "revoked"
        self._save_users()
        Logger.security(f"User revoked: {username}")
        return {"status": "ok", "message": "User revoked successfully"}

    # Helpers

    def get_user(self, username: str):
        return self.users.get(username.lower().strip())

    def get_user_key(self, username: str):
        # Return long-term AES key as bytes, or None.
        user = self.get_user(username)
        if not user:
            return None
        return bytes.fromhex(user["long_term_key"])

    def get_all_users_summary(self):
        # Return non-sensitive info for admin listing.
        summary = {}
        for uname, u in self.users.items():
            summary[uname] = {
                "role": u["role"],
                "status": u["status"],
                "key_id": u["key_id"],
                "created_at": u["created_at"],
            }
        return summary

    def _save_users(self):
        self.storage.save_encrypted(USER_FILE, self.users)
