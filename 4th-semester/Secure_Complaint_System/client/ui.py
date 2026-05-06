# client/ui.py
import os
import time


class UI:
    
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pause():
        input("\nPress ENTER to continue...")

    @staticmethod
    def header(title: str):
        UI.clear()
        print("=" * 50)
        print(f" {title}")
        print("=" * 50)

    @staticmethod
    def print_banner():
        UI.clear()
        banner = r"""
   ____                      ____                           _ _       _   
  / ___|  ___  __ _ _ __   / ___|___  _ __  _ __   ___  __| (_) __ _| |_ 
  \___ \ / _ \/ _` | '_ \ | |   / _ \| '_ \| '_ \ / _ \/ _` | |/ _` | __|
   ___) |  __/ (_| | | | || |__| (_) | | | | | | |  __/ (_| | | (_| | |_ 
  |____/ \___|\__,_|_| |_| \____\___/|_| |_|_| |_|\___|\__,_|_|\__,_|\__|
        """
        print(banner)
        print("\nWelcome to the Secure Complaint System\n")

    @staticmethod
    def login_menu():
        UI.print_banner()
        print("1) Login")
        print("2) Register")
        print("0) Exit")
        print("-" * 50)
        return input("Select option: ").strip()


    @staticmethod
    def user_menu(username: str):
        UI.header(f"User Menu — Logged in as: {username}")
        print("1) Submit Complaint")
        print("2) View My Complaints")
        print("3) View Replies to My Complaints")
        print("4) Chat")
        print("0) Logout")
        print("-" * 50)
        return input("Select option: ").strip()


    @staticmethod
    def admin_menu(username: str):
        UI.header(f"Admin Menu — Logged in as: {username}")
        print("1) View All Complaints")
        print("2) Reply to a Complaint")
        print("3) Rotate User Key")
        print("4) Revoke User")
        print("5) View Blockchain Validity")
        print("6) View Users / Keys / Status")
        print("7) View Replies for a Specific User")
        print("8) View Integrity Status")
        print("9) Chat")
        print("0) Logout")
        print("-" * 50)
        return input("Select option: ").strip()


    @staticmethod
    def display_complaint(comp: dict):
        print("-" * 50)
        print(f"Complaint ID:   {comp.get('complaint_id')}")
        print(f"User:           {comp.get('user')}")
        print(f"IV:             {comp.get('iv')[:16]}...")
        print(f"Ciphertext:     {comp.get('ciphertext')[:16]}...")
        print(f"Timestamp:      {time.ctime(comp.get('timestamp'))}")
        print(f"Replies:        {len(comp.get('replies', []))}")
        print("-" * 50)

    @staticmethod
    def display_reply(rep: dict):
        print("-" * 50)
        print(f"Reply ID:       {rep.get('reply_id')}")
        print(f"Complaint ID:   {rep.get('complaint_id')}")
        print(f"IV:             {rep.get('iv')[:16]}...")
        print(f"Ciphertext:     {rep.get('ciphertext')[:16]}...")
        print(f"Timestamp:      {time.ctime(rep.get('timestamp'))}")
        print("-" * 50)
