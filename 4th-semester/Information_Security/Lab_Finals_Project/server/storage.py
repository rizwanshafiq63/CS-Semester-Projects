# server/storage.py

import json
import os

from crypto.crypto_utils import (
    aes_encrypt_cbc,
    aes_decrypt_cbc,
    generate_aes_key,
    hash_sha256,
)
from server.logger import Logger


DATA_DIR = "data"
USER_FILE = f"{DATA_DIR}/users.json.enc"
COMPLAINT_FILE = f"{DATA_DIR}/complaints.json.enc"
REPLY_FILE = f"{DATA_DIR}/replies.json.enc"
BLOCKCHAIN_FILE = f"{DATA_DIR}/blockchain.json"
MASTER_KEY_FILE = f"{DATA_DIR}/master.key"
INTEGRITY_FILE = f"{DATA_DIR}/.integrity"


class SecureStorage:

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(f"{DATA_DIR}/logs", exist_ok=True)

        self.master_key = self._load_or_create_master_key()
        Logger.security("Master key initialized for encrypted storage")

        # Load or initialize integrity map
        self.integrity_map = self._load_integrity_file()

    # Master key loading / creation
    def _load_or_create_master_key(self):
        if os.path.exists(MASTER_KEY_FILE):
            with open(MASTER_KEY_FILE, "rb") as f:
                key = f.read()
                Logger.info("Loaded master key from disk")
                return key

        # create new key
        key = generate_aes_key()
        with open(MASTER_KEY_FILE, "wb") as f:
            f.write(key)
        Logger.success("Generated new master key")
        return key

    # Integrity file handling

    def _load_integrity_file(self) -> dict:
        """
        Structure:
        {
          "users": {
             "hash": "<sha256 hex of encrypted users.json.enc content>",
             "timestamp": "...",
             "filename": "users.json.enc"
          },
          ...
        }
        """
        if not os.path.exists(INTEGRITY_FILE):
            Logger.warning(f"Integrity file missing: {INTEGRITY_FILE} → starting fresh")
            return {}

        try:
            with open(INTEGRITY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            Logger.info("Loaded integrity metadata")
            return data
        except Exception:
            Logger.error("Failed to load integrity file, starting with empty integrity map")
            return {}

    def _save_integrity_file(self):
        try:
            with open(INTEGRITY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.integrity_map, f, indent=2)
            Logger.info("Updated integrity metadata")
        except Exception as e:
            Logger.error(f"Failed to update integrity file: {e}")

    def _infer_file_type(self, filename: str) -> str | None:
        if filename == USER_FILE:
            return "users"
        if filename == COMPLAINT_FILE:
            return "complaints"
        if filename == REPLY_FILE:
            return "replies"
        return None

    def _update_integrity_hash(self, filename: str, enc_obj: dict):
        file_type = self._infer_file_type(filename)
        if file_type is None:
            return

        # Compute hash over the encrypted JSON string (stable, sorted keys)
        enc_str = json.dumps(enc_obj, sort_keys=True)
        h = hash_sha256(enc_str)

        from time import strftime, localtime
        ts = strftime("%Y-%m-%d %H:%M:%S", localtime())

        self.integrity_map[file_type] = {
            "hash": h,
            "timestamp": ts,
            "filename": os.path.basename(filename),
        }
        self._save_integrity_file()
        Logger.security(f"Updated integrity hash for {file_type} ({filename})")

    def _verify_integrity(self, filename: str, enc_obj: dict) -> bool:
        file_type = self._infer_file_type(filename)
        if file_type is None:
            # Unknown file type → can't verify
            Logger.warning(f"No integrity type mapping for file: {filename}")
            return False

        record = self.integrity_map.get(file_type)
        if not record:
            Logger.warning(f"No integrity record for '{file_type}' – cannot verify tampering")
            return False

        expected_hash = record.get("hash")
        enc_str = json.dumps(enc_obj, sort_keys=True)
        current_hash = hash_sha256(enc_str)

        if current_hash == expected_hash:
            Logger.security(f"Integrity verified for {file_type}")
            return True
        else:
            Logger.error(f"INTEGRITY VIOLATION for {file_type}! Hash mismatch.")
            return False

    # JSON encryption helpers

    def _encrypt_json(self, obj: dict) -> dict:
        """
        Returns a dict containing:
            {
                "iv": "...hex...",
                "ciphertext": "...hex..."
            }
        where ciphertext is AES-256-CBC over the JSON string.
        """
        json_str = json.dumps(obj)
        iv_hex, ct_hex = aes_encrypt_cbc(self.master_key, json_str)
        return {"iv": iv_hex, "ciphertext": ct_hex}

    def _decrypt_json(self, enc_obj: dict) -> dict:
        iv = enc_obj.get("iv")
        ct = enc_obj.get("ciphertext")
        decrypted = aes_decrypt_cbc(self.master_key, iv, ct)
        return json.loads(decrypted)

    # Write / load encrypted JSON file (with integrity)

    def save_encrypted(self, filename: str, obj: dict):
        enc = self._encrypt_json(obj)

        # Save encrypted file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(enc, f)
        Logger.info(f"Saved encrypted file: {filename}")

        # Update integrity hash for this encrypted content
        self._update_integrity_hash(filename, enc)

    def load_encrypted(self, filename: str) -> dict:
        if not os.path.exists(filename):
            Logger.warning(f"Encrypted file missing: {filename} → returning empty dict")
            return {}

        try:
            with open(filename, "r", encoding="utf-8") as f:
                enc = json.load(f)
        except Exception as e:
            Logger.error(f"Failed to read encrypted file {filename}: {e}")
            return {}

        # Verify integrity BEFORE decrypting
        if not self._verify_integrity(filename, enc):
            Logger.error(f"Refusing to decrypt {filename} due to integrity failure")
            return {}

        try:
            return self._decrypt_json(enc)
        except Exception as e:
            Logger.error(f"Failed to decrypt {filename}, returning empty dict: {e}")
            return {}

    def get_integrity_status(self) -> dict:
        import json as _json
        status = {}

        files = [
            ("users", USER_FILE),
            ("complaints", COMPLAINT_FILE),
            ("replies", REPLY_FILE),
        ]

        for file_type, path in files:
            entry = {"exists": False, "integrity_ok": False, "message": ""}

            if not os.path.exists(path):
                entry["message"] = "File not found"
                status[file_type] = entry
                continue

            entry["exists"] = True

            try:
                with open(path, "r", encoding="utf-8") as f:
                    enc = _json.load(f)
            except Exception as e:
                entry["message"] = f"Failed to read file: {e}"
                status[file_type] = entry
                continue

            # Use existing internal integrity check
            ok = self._verify_integrity(path, enc)
            entry["integrity_ok"] = ok
            entry["message"] = "Integrity OK" if ok else "INTEGRITY VIOLATION"
            status[file_type] = entry

        return status


    # Blockchain storage 

    def backup_blockchain(self, chain_list: list):
        # Saves blockchain to data/blockchain.json (unencrypted), for demonstration / debugging purposes.
        try:
            with open(BLOCKCHAIN_FILE, "w", encoding="utf-8") as f:
                json.dump(chain_list, f, indent=2)
            Logger.blockchain("Blockchain snapshot saved")
        except Exception as e:
            Logger.error(f"Failed to backup blockchain: {e}")
