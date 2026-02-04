# server/server.py

import json
import socket
import threading
import time
from typing import Dict, Any

from crypto.crypto_utils import generate_id
from server.logger import Logger
from server.storage import SecureStorage
from server.key_manager import KeyManager
from server.complaint_manager import ComplaintManager


HOST = "127.0.0.1"
PORT = 9090


class SecureComplaintServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        self.storage = SecureStorage()
        self.key_manager = KeyManager(self.storage)
        self.complaint_manager = ComplaintManager(self.storage, self.key_manager)

        self.chat_requests: Dict[str, Dict[str, Any]] = {}
        self.chat_sessions: Dict[str, Dict[str, Any]] = {}
        self.chat_inbox: Dict[str, list] = {}

        Logger.success("Secure Complaint Server initialized")

    # Networking

    def handle_client(self, conn: socket.socket, addr):
        Logger.info(f"Client connected → {addr}")
        try:
            f = conn.makefile("rwb")
            while True:
                line = f.readline()
                if not line:
                    break

                try:
                    request = json.loads(line.decode("utf-8").strip())
                except json.JSONDecodeError:
                    Logger.error("Invalid JSON from client")
                    self._send_json(f, {"status": "error", "message": "Invalid JSON"})
                    continue

                action = request.get("action")
                response = self.dispatch(action, request)
                self._send_json(f, response)
        except Exception as e:
            Logger.error(f"Client handler exception: {e}")
        finally:
            conn.close()
            Logger.warning(f"Client disconnected → {addr}")

    def _send_json(self, f, obj: Dict[str, Any]):
        data = (json.dumps(obj) + "\n").encode("utf-8")
        f.write(data)
        f.flush()

    # Dispatcher

    def dispatch(self, action: str, req: Dict[str, Any]) -> Dict[str, Any]:
        Logger.info(f"Action requested → {action}")

        # 1) Authentication
        if action == "register":
            return self.key_manager.register_user(
                username=req.get("username", ""),
                password=req.get("password", ""),
                role=req.get("role", "user"),
            )

        if action == "login":
            return self.key_manager.login(
                username=req.get("username", ""),
                password=req.get("password", ""),
            )

        # 2) Session key 
        if action == "request_session_key":
            return self.key_manager.issue_session_key()

        def ensure_active(username: str):
            u = self.key_manager.get_user(username)
            if not u:
                return {"status": "error", "message": "User not found"}
            if u["status"] != "active":
                return {"status": "error", "message": f"User is {u['status']}"}
            return {"status": "ok"}

        def _inbox_for(username: str) -> list:
            username = username.lower().strip()
            if username not in self.chat_inbox:
                self.chat_inbox[username] = []
            return self.chat_inbox[username]

        # Chat
        if action == "chat_request":
            from_user = req.get("from", "").lower().strip()
            to_user = req.get("to", "").lower().strip()

            chk_from = ensure_active(from_user)
            if chk_from["status"] != "ok":
                return chk_from
            chk_to = ensure_active(to_user)
            if chk_to["status"] != "ok":
                return chk_to

            if from_user == to_user:
                return {"status": "error", "message": "Cannot chat with yourself"}

            req_id = generate_id("CHATREQ")
            self.chat_requests[req_id] = {
                "id": req_id,
                "from": from_user,
                "to": to_user,
                "timestamp": time.time(),
                "status": "pending",
            }

            _inbox_for(to_user).append({
                "type": "chat_request",
                "request_id": req_id,
                "from": from_user,
                "timestamp": time.time(),
            })

            Logger.security(f"Chat request created {req_id}: {from_user} -> {to_user}")
            return {"status": "ok", "message": "Chat request sent", "request_id": req_id}

        if action == "chat_fetch":
            username = req.get("username", "").lower().strip()
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            inbox = _inbox_for(username)
            events = inbox[:]
            inbox.clear()
            return {"status": "ok", "events": events}

        if action == "chat_accept":
            username = req.get("username", "").lower().strip()
            request_id = req.get("request_id", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk

            r = self.chat_requests.get(request_id)
            if not r or r.get("status") != "pending":
                return {"status": "error", "message": "Invalid or expired request"}
            if r.get("to") != username:
                return {"status": "error", "message": "Not authorized for this request"}

            chat_id = generate_id("CHAT")
            sess = self.key_manager.issue_session_key()
            session_key_hex = sess.get("session_key_hex")
            self.chat_sessions[chat_id] = {
                "chat_id": chat_id,
                "admin": r["from"],
                "user": r["to"],
                "session_key_hex": session_key_hex,
                "active": True,
                "created_at": time.time(),
            }
            r["status"] = "accepted"

            _inbox_for(r["from"]).append({
                "type": "chat_started",
                "chat_id": chat_id,
                "peer": r["to"],
                "session_key_hex": session_key_hex,
                "timestamp": time.time(),
            })
            _inbox_for(r["to"]).append({
                "type": "chat_started",
                "chat_id": chat_id,
                "peer": r["from"],
                "session_key_hex": session_key_hex,
                "timestamp": time.time(),
            })

            Logger.security(f"Chat accepted {chat_id}: {r['from']} <-> {r['to']}")
            return {"status": "ok", "message": "Chat started", "chat_id": chat_id, "session_key_hex": session_key_hex, "peer": r["from"]}

        if action == "chat_reject":
            username = req.get("username", "").lower().strip()
            request_id = req.get("request_id", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            r = self.chat_requests.get(request_id)
            if not r or r.get("status") != "pending":
                return {"status": "error", "message": "Invalid or expired request"}
            if r.get("to") != username:
                return {"status": "error", "message": "Not authorized for this request"}
            r["status"] = "rejected"
            _inbox_for(r["from"]).append({
                "type": "chat_rejected",
                "request_id": request_id,
                "by": username,
                "timestamp": time.time(),
            })
            Logger.security(f"Chat request rejected {request_id} by {username}")
            return {"status": "ok", "message": "Chat request rejected"}

        if action == "chat_send":
            username = req.get("username", "").lower().strip()
            chat_id = req.get("chat_id", "")
            iv = req.get("iv", "")
            ciphertext = req.get("ciphertext", "")

            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk

            sess = self.chat_sessions.get(chat_id)
            if not sess or not sess.get("active"):
                return {"status": "error", "message": "Chat not active"}

            if username not in (sess["admin"], sess["user"]):
                return {"status": "error", "message": "Not a participant of this chat"}

            other = sess["user"] if username == sess["admin"] else sess["admin"]

            _inbox_for(other).append({
                "type": "chat_message",
                "chat_id": chat_id,
                "from": username,
                "iv": iv,
                "ciphertext": ciphertext,
                "timestamp": time.time(),
            })
            return {"status": "ok", "message": "Message delivered"}

        if action == "chat_end":
            username = req.get("username", "").lower().strip()
            chat_id = req.get("chat_id", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk

            sess = self.chat_sessions.get(chat_id)
            if not sess or not sess.get("active"):
                return {"status": "error", "message": "Chat not active"}

            if username not in (sess["admin"], sess["user"]):
                return {"status": "error", "message": "Not a participant of this chat"}

            sess["active"] = False
            sess["session_key_hex"] = ""
            other = sess["user"] if username == sess["admin"] else sess["admin"]
            _inbox_for(other).append({
                "type": "chat_ended",
                "chat_id": chat_id,
                "by": username,
                "timestamp": time.time(),
            })
            Logger.security(f"Chat ended {chat_id} by {username}")
            return {"status": "ok", "message": "Chat ended"}

        # 3) User: submit complaint
        if action == "submit_complaint":
            username = req.get("username", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            text = req.get("text", "")
            return self.complaint_manager.submit_complaint(username, text)

        # 4) User: get own complaints
        if action == "get_user_complaints":
            username = req.get("username", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            return {
                "status": "ok",
                "complaints": self.complaint_manager.get_user_complaints(username)
            }

        # 5) Admin: get all complaints
        if action == "get_all_complaints":
            return {
                "status": "ok",
                "complaints": self.complaint_manager.get_all_complaints()
            }

        # 6) Admin: reply to complaint
        if action == "reply_to_complaint":
            cid = req.get("complaint_id", "")
            reply_text = req.get("reply_text", "")
            return self.complaint_manager.reply_to_complaint(cid, reply_text)

        # 7) User: get replies for themselves
        if action == "get_replies_for_user":
            username = req.get("username", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            return {
                "status": "ok",
                "replies": self.complaint_manager.get_replies_for_user(username)
            }

        # 8) User: decrypt specific reply
        if action == "decrypt_reply_user":
            username = req.get("username", "")
            reply_id = req.get("reply_id", "")
            chk = ensure_active(username)
            if chk["status"] != "ok":
                return chk
            return self.complaint_manager.decrypt_reply_for_user(username, reply_id)

        # 9) Admin: decrypt complaint
        if action == "decrypt_complaint_admin":
            complaint_id = req.get("complaint_id", "")
            return self.complaint_manager.decrypt_complaint_admin(complaint_id)

        # 10) Admin: rotate key & revoke
        if action == "rotate_user_key":
            return self.key_manager.rotate_user_key(req.get("username", ""))

        if action == "revoke_user":
            return self.key_manager.revoke_user(req.get("username", ""))

        # 11) Blockchain validity
        if action == "verify_blockchain":
            valid = self.complaint_manager.is_blockchain_valid()
            return {"status": "ok", "valid": valid}

        # 12) User status summary
        if action == "get_user_status":
            return {
                "status": "ok",
                "users": self.key_manager.get_all_users_summary()
            }

        # 13) Integrity status (users / complaints / replies)
        if action == "get_integrity_status":
            return {
                "status": "ok",
                "files": self.storage.get_integrity_status(),
            }

        # Unknown
        Logger.error(f"Unknown action requested: {action}")
        return {"status": "error", "message": f"Unknown action '{action}'"}

    # Start server

    def start(self):
        Logger.info(f"Starting Secure Complaint Server at {self.host}:{self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            Logger.success("Server is now listening for clients...")
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                t.start()


if __name__ == "__main__":
    server = SecureComplaintServer()
    server.start()
