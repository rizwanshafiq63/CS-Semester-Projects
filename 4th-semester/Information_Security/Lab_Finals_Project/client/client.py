# client/client.py

import json
import socket
from typing import Dict, Any

from client.ui import UI
from client.crypto_client import ClientCrypto

from crypto.crypto_utils import aes_encrypt_cbc, aes_decrypt_cbc

HOST = "127.0.0.1"
PORT = 9090


class ClientApp:

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        self.sock = None
        self.file = None

        self.username = None
        self.role = None

        self.crypto = None 

        self.chat_sessions: Dict[str, Dict[str, Any]] = {}
        self.pending_chat_requests: Dict[str, Dict[str, Any]] = {}

    # Networking

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.file = self.sock.makefile("rwb")
        self.crypto = ClientCrypto(self.send_request)
        UI.clear()
        print(f"[+] Connected to server {self.host}:{self.port}")

    def disconnect(self):
        if self.file:
            self.file.close()
        if self.sock:
            self.sock.close()
        print("[*] Disconnected from server")

    def send_request(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        if not self.file:
            raise RuntimeError("Not connected to server")

        self.file.write((json.dumps(obj) + "\n").encode("utf-8"))
        self.file.flush()

        line = self.file.readline()
        if not line:
            raise RuntimeError("Server closed connection")
        return json.loads(line.decode("utf-8").strip())

    # Authentication

    def register(self):
        UI.header("Register")
        username = input("Choose username: ").strip()
        password = input("Choose password: ").strip()
        role = input("Role (user/admin, default user): ").strip() or "user"

        resp = self.send_request({
            "action": "register",
            "username": username,
            "password": password,
            "role": role,
        })
        print("->", resp.get("message"))
        UI.pause()

    def login(self):
        UI.header("Login")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        resp = self.send_request({
            "action": "login",
            "username": username,
            "password": password,
        })
        if resp.get("status") == "ok":
            self.username = username
            self.role = resp.get("role")
            print(f"[+] Login successful as {username} ({self.role})")
        else:
            print("->", resp.get("message"))
        UI.pause()

    # User Functions

    def user_submit_complaint(self):
        UI.header("Submit Complaint")
        text = input("Enter your complaint text: ").strip()

        resp = self.send_request({
            "action": "submit_complaint",
            "username": self.username,
            "text": text,
        })
        print("->", resp.get("message"))
        if resp.get("status") == "ok":
            print(f"Complaint ID: {resp['complaint_id']}")
            print(f"Block Index: {resp['block_index']}")
        UI.pause()

    def user_view_complaints(self):
        UI.header("My Complaints")
        resp = self.send_request({
            "action": "get_user_complaints",
            "username": self.username,
        })
        complaints = resp.get("complaints", [])
        if not complaints:
            print("No complaints submitted yet.")
            UI.pause()
            return
        for comp in complaints:
            UI.display_complaint(comp)
        UI.pause()

    def user_view_replies(self):
        UI.header("Replies to My Complaints")
        resp = self.send_request({
            "action": "get_replies_for_user",
            "username": self.username,
        })
        replies = resp.get("replies", [])
        if not replies:
            print("No replies yet.")
            UI.pause()
            return

        for rep in replies:
            UI.display_reply(rep)

        dec = input("\nDecrypt a reply? (y/n): ").strip().lower()
        if dec == "y":
            rid = input("Enter Reply ID: ").strip()
            resp2 = self.send_request({
                "action": "decrypt_reply_user",
                "username": self.username,
                "reply_id": rid,
            })
            if resp2.get("status") == "ok":
                print("\n=== Reply Plaintext ===")
                print(resp2.get("plaintext"))
            else:
                print("->", resp2.get("message"))
            UI.pause()

    # Admin Functions

    def admin_view_complaints(self):
        UI.header("All Complaints (Admin)")
        resp = self.send_request({
            "action": "get_all_complaints"
        })
        complaints = resp.get("complaints", [])
        if not complaints:
            print("No complaints found.")
            UI.pause()
            return

        for comp in complaints:
            UI.display_complaint(comp)

        dec = input("\nDecrypt a complaint? (y/n): ").strip().lower()
        if dec == "y":
            cid = input("Enter Complaint ID: ").strip()
            resp2 = self.send_request({
                "action": "decrypt_complaint_admin",
                "complaint_id": cid,
            })
            if resp2.get("status") == "ok":
                print("\n=== Complaint Plaintext ===")
                print(resp2.get("plaintext"))
            else:
                print("->", resp2.get("message"))
        UI.pause()

    def admin_reply_to_complaint(self):
        UI.header("Reply to Complaint")
        cid = input("Enter Complaint ID: ").strip()
        reply_text = input("Enter reply message: ").strip()

        resp = self.send_request({
            "action": "reply_to_complaint",
            "complaint_id": cid,
            "reply_text": reply_text,
        })
        print("->", resp.get("message"))
        UI.pause()

    def admin_rotate_key(self):
        UI.header("Rotate User Key")
        uname = input("Username to rotate key for: ").strip()
        resp = self.send_request({
            "action": "rotate_user_key",
            "username": uname,
        })
        print("->", resp.get("message"))
        UI.pause()

    def admin_revoke_user(self):
        UI.header("Revoke User")
        uname = input("Username to revoke: ").strip()
        resp = self.send_request({
            "action": "revoke_user",
            "username": uname,
        })
        print("->", resp.get("message"))
        UI.pause()

    def admin_view_replies_for_user(self):
        UI.header("Replies for Specific User")
        uname = input("Username: ").strip()
        resp = self.send_request({
            "action": "get_replies_for_user",
            "username": uname,
        })
        replies = resp.get("replies", [])
        if not replies:
            print("No replies.")
            UI.pause()
            return
        for rep in replies:
            UI.display_reply(rep)
        UI.pause()

    def admin_blockchain_validity(self):
        UI.header("Blockchain Validity")
        resp = self.send_request({"action": "verify_blockchain"})
        valid = resp.get("valid")
        print("-> Blockchain is VALID" if valid else "-> Blockchain is INVALID")
        UI.pause()

    def admin_view_user_status(self):
        UI.header("User / Key Status")
        resp = self.send_request({"action": "get_user_status"})
        if resp.get("status") != "ok":
            print("->", resp.get("message"))
            UI.pause()
            return

        users = resp.get("users", {})
        if not users:
            print("No users registered yet.")
            UI.pause()
            return

        for uname, info in users.items():
            print("-" * 50)
            print(f"Username:   {uname}")
            print(f"Role:       {info['role']}")
            print(f"Status:     {info['status']}")
            print(f"Key ID:     {info['key_id']}")
            print(f"Created at: {info['created_at']}")
        UI.pause()
    
    def admin_view_integrity(self):
        UI.header("Integrity Status (Encrypted Storage)")

        req = {"action": "get_integrity_status"}
        resp = self.send_request(req)

        if resp.get("status") != "ok":
            print("->", resp.get("message"))
            UI.pause()
            return

        files = resp.get("files", {})

        for ftype, info in files.items():
            print("-" * 50)
            print(f"File Type:     {ftype}")
            print(f"Exists:        {info.get('exists')}")
            print(f"Integrity OK:  {info.get('integrity_ok')}")
            print(f"Message:       {info.get('message')}")
        print("-" * 50)
        UI.pause()

    def chat_fetch_events(self):
        resp = self.send_request({"action": "chat_fetch", "username": self.username})
        if resp.get("status") != "ok":
            return []
        return resp.get("events", [])

    def chat_process_events(self, events):
        for ev in events:
            et = ev.get("type")
            if et == "chat_request":
                rid = ev.get("request_id")
                self.pending_chat_requests[rid] = ev
                print(f"[CHAT] Incoming chat request from {ev.get('from')} (request_id={rid})")

            elif et == "chat_started":
                chat_id = ev.get("chat_id")
                key_hex = ev.get("session_key_hex", "")
                peer = ev.get("peer", "")
                if chat_id and key_hex:
                    self.chat_sessions[chat_id] = {"key": bytes.fromhex(key_hex), "peer": peer}
                    print(f"[CHAT] Chat started with {peer} (chat_id={chat_id})")

            elif et == "chat_rejected":
                print(f"[CHAT] Chat request rejected by {ev.get('by')}")

            elif et == "chat_ended":
                chat_id = ev.get("chat_id")
                by = ev.get("by")
                if chat_id in self.chat_sessions:
                    del self.chat_sessions[chat_id]
                print(f"[CHAT] Chat ended by {by} (chat_id={chat_id})")

            elif et == "chat_message":
                chat_id = ev.get("chat_id")
                sender = ev.get("from")
                sess = self.chat_sessions.get(chat_id)
                if not sess:
                    print(f"[CHAT] Message for unknown chat_id={chat_id}")
                    continue
                key = sess["key"]
                try:
                    msg = aes_decrypt_cbc(key, ev.get("iv", ""), ev.get("ciphertext", ""))
                except Exception:
                    msg = "<decryption failed>"
                print(f"[CHAT] {sender}: {msg}")

    def chat_end_all(self):
        for chat_id in list(self.chat_sessions.keys()):
            try:
                self.send_request({"action": "chat_end", "username": self.username, "chat_id": chat_id})
            except Exception:
                pass
        self.chat_sessions.clear()
        self.pending_chat_requests.clear()

    def chat_menu(self):
        UI.header("Chat")
        events = self.chat_fetch_events()
        if events:
            self.chat_process_events(events)
        else:
            print("No new chat events.")

        while True:
            print("\n1) Fetch chat events")
            if self.role == "admin":
                print("2) Request chat with user")
            if self.pending_chat_requests:
                print("3) Respond to pending requests")
            if self.chat_sessions:
                print("4) Send message")
                print("5) End chat")
            print("0) Back")
            choice = input("Select option: ").strip()

            if choice == "0":
                return

            if choice == "1":
                UI.header("Chat")
                events = self.chat_fetch_events()
                if events:
                    self.chat_process_events(events)
                else:
                    print("No new chat events.")
                continue

            if choice == "2" and self.role == "admin":
                to_user = input("Enter username to chat with: ").strip()
                resp = self.send_request({"action": "chat_request", "from": self.username, "to": to_user})
                print(resp.get("message"))
                continue

            if choice == "3" and self.pending_chat_requests:
                rid = input("Enter request_id to respond: ").strip()
                if rid not in self.pending_chat_requests:
                    print("Invalid request_id.")
                    continue
                resp_choice = input("Accept? (y/n): ").strip().lower()
                if resp_choice == "y":
                    resp = self.send_request({"action": "chat_accept", "username": self.username, "request_id": rid})
                    print(resp.get("message"))
                else:
                    resp = self.send_request({"action": "chat_reject", "username": self.username, "request_id": rid})
                    print(resp.get("message"))
                del self.pending_chat_requests[rid]
                continue

            if choice == "4" and self.chat_sessions:
                print("\nActive chats:")
                items = list(self.chat_sessions.items())
                for i, (cid, sess) in enumerate(items, start=1):
                    print(f"{i}) {sess.get('peer')}  — chat_id: {cid}")

                sel = input("\nSelect chat number: ").strip()
                if not sel.isdigit() or not (1 <= int(sel) <= len(items)):
                    print("Invalid selection.")
                    continue

                chat_id, sess = items[int(sel) - 1]

                msg = input("Message: ")
                iv_hex, ct_hex = aes_encrypt_cbc(sess["key"], msg)
                resp = self.send_request({
                    "action": "chat_send",
                    "username": self.username,
                    "chat_id": chat_id,
                    "iv": iv_hex,
                    "ciphertext": ct_hex
                })
                if resp.get("status") != "ok":
                    print(resp.get("message"))
                continue

            if choice == "5" and self.chat_sessions:
                chat_id = input("Enter chat_id to end: ").strip()
                resp = self.send_request({"action": "chat_end", "username": self.username, "chat_id": chat_id})
                print(resp.get("message"))
                if chat_id in self.chat_sessions:
                    del self.chat_sessions[chat_id]
                continue

            print("Invalid option.")

    # Main Flow

    def run(self):
        self.connect()
        try:
            while True:
                choice = UI.login_menu()
                if choice == "1":
                    self.login()
                    if self.username:
                        break
                elif choice == "2":
                    self.register()
                elif choice == "0":
                    return
                else:
                    print("Invalid choice.")
                    UI.pause()

            if self.role == "user":
                self.user_loop()
            else:
                self.admin_loop()
        finally:
            self.disconnect()

    def user_loop(self):
        while True:
            choice = UI.user_menu(self.username)
            if choice == "1":
                self.user_submit_complaint()
            elif choice == "2":
                self.user_view_complaints()
            elif choice == "3":
                self.user_view_replies()
            elif choice == "4":
                self.chat_menu()
            elif choice == "0":
                self.chat_end_all()
                return
            else:
                print("Invalid option")
                UI.pause()

    def admin_loop(self):
        while True:
            choice = UI.admin_menu(self.username)
            if choice == "1":
                self.admin_view_complaints()
            elif choice == "2":
                self.admin_reply_to_complaint()
            elif choice == "3":
                self.admin_rotate_key()
            elif choice == "4":
                self.admin_revoke_user()
            elif choice == "5":
                self.admin_blockchain_validity()
            elif choice == "6":
                self.admin_view_user_status()
            elif choice == "7":
                self.admin_view_replies_for_user()
            elif choice == "8":
                self.admin_view_integrity()
            elif choice == "9":
                self.chat_menu()
            elif choice == "0":
                self.chat_end_all()
                return
            else:
                print("Invalid option")
                UI.pause()


if __name__ == "__main__":
    app = ClientApp()
    app.run()
