import time
from typing import Dict, Any, List

from crypto.crypto_utils import (
    aes_decrypt_cbc,
    aes_encrypt_cbc,
    generate_human_readable_id
)
from blockchain.blockchain import Blockchain
from server.logger import Logger
from server.storage import (
    COMPLAINT_FILE,
    REPLY_FILE,
    SecureStorage
)
from server.key_manager import KeyManager


class ComplaintManager:
    def __init__(self, storage: SecureStorage, key_manager: KeyManager):
        self.storage = storage
        self.key_manager = key_manager

        self.complaints: Dict[str, Dict[str, Any]] = storage.load_encrypted(COMPLAINT_FILE)
        if not isinstance(self.complaints, dict):
            self.complaints = {}

        self.replies: Dict[str, Dict[str, Any]] = storage.load_encrypted(REPLY_FILE)
        if not isinstance(self.replies, dict):
            self.replies = {}

        self.blockchain = Blockchain()
        Logger.info("Complaint Manager initialized")


    def submit_complaint(self, username: str, plaintext: str) -> Dict[str, Any]:
        key = self.key_manager.get_user_key(username)
        if key is None:
            return {"status": "error", "message": "User key not found"}

        iv_hex, ct_hex = aes_encrypt_cbc(key, plaintext)
        complaint_id = generate_human_readable_id("CMP")

        record = {
            "complaint_id": complaint_id,
            "user": username,
            "iv": iv_hex,
            "ciphertext": ct_hex,
            "timestamp": time.time(),
            "replies": []
        }

        self.complaints[complaint_id] = record
        self._save_complaints()

        block = self.blockchain.add_block({
            "type": "complaint",
            "complaint_id": complaint_id,
            "user": username,
            "iv": iv_hex,
            "ciphertext": ct_hex,
        })

        self.storage.backup_blockchain(self.blockchain.to_list())
        Logger.blockchain(f"Added complaint block #{block.index} with id {complaint_id}")

        return {
            "status": "ok",
            "message": "Complaint stored successfully",
            "complaint_id": complaint_id,
            "block_index": block.index,
            "block_hash": block.hash,
        }


    def reply_to_complaint(self, complaint_id: str, reply_text: str) -> Dict[str, Any]:
        comp = self.complaints.get(complaint_id)
        if not comp:
            Logger.warning(f"Reply failed — complaint not found: {complaint_id}")
            return {"status": "error", "message": "Complaint not found"}

        username = comp["user"]
        key = self.key_manager.get_user_key(username)
        if key is None:
            return {"status": "error", "message": "User key not found"}

        iv_hex, ct_hex = aes_encrypt_cbc(key, reply_text)
        reply_id = generate_human_readable_id("RPL")

        reply_record = {
            "reply_id": reply_id,
            "complaint_id": complaint_id,
            "iv": iv_hex,
            "ciphertext": ct_hex,
            "timestamp": time.time(),
        }

        self.replies[reply_id] = reply_record
        self._save_replies()

        self.complaints[complaint_id]["replies"].append(reply_id)
        self._save_complaints()

        block = self.blockchain.add_block({
            "type": "reply",
            "reply_id": reply_id,
            "complaint_id": complaint_id,
            "iv": iv_hex,
            "ciphertext": ct_hex,
        })

        self.storage.backup_blockchain(self.blockchain.to_list())
        Logger.blockchain(f"Added reply block #{block.index} for complaint {complaint_id}")

        return {
            "status": "ok",
            "message": "Reply stored successfully",
            "reply_id": reply_id,
            "block_index": block.index,
            "block_hash": block.hash,
        }


    def get_user_complaints(self, username: str) -> List[Dict[str, Any]]:
        return [c for c in self.complaints.values() if c["user"] == username]

    def get_all_complaints(self) -> List[Dict[str, Any]]:
        return list(self.complaints.values())

    def get_replies_for_user(self, username: str):
        result = []
        for r in self.replies.values():
            cid = r["complaint_id"]
            comp = self.complaints.get(cid)
            if comp and comp["user"] == username:
                result.append(r)
        return result


    def decrypt_complaint_admin(self, complaint_id: str) -> Dict[str, Any]:
        comp = self.complaints.get(complaint_id)
        if not comp:
            return {"status": "error", "message": "Complaint not found"}

        username = comp["user"]
        key = self.key_manager.get_user_key(username)
        if not key:
            return {"status": "error", "message": "User key not found"}

        try:
            plaintext = aes_decrypt_cbc(key, comp["iv"], comp["ciphertext"])
            return {"status": "ok", "plaintext": plaintext}
        except Exception:
            return {"status": "error", "message": "Decryption failed"}

    def decrypt_reply_for_user(self, username: str, reply_id: str) -> Dict[str, Any]:
        rep = self.replies.get(reply_id)
        if not rep:
            return {"status": "error", "message": "Reply not found"}

        cid = rep["complaint_id"]
        comp = self.complaints.get(cid)
        if not comp or comp["user"] != username:
            return {"status": "error", "message": "Not authorized for this reply"}

        key = self.key_manager.get_user_key(username)
        if not key:
            return {"status": "error", "message": "User key not found"}

        try:
            plaintext = aes_decrypt_cbc(key, rep["iv"], rep["ciphertext"])
            return {"status": "ok", "plaintext": plaintext}
        except Exception:
            return {"status": "error", "message": "Decryption failed"}


    def is_blockchain_valid(self) -> bool:
        return self.blockchain.is_valid()


    def _save_complaints(self):
        self.storage.save_encrypted(COMPLAINT_FILE, self.complaints)

    def _save_replies(self):
        self.storage.save_encrypted(REPLY_FILE, self.replies)
