# run_server.py

from server.server import SecureComplaintServer

if __name__ == "__main__":
    print("\nStarting Secure Complaint System Server...\n")
    server = SecureComplaintServer()
    server.start()
