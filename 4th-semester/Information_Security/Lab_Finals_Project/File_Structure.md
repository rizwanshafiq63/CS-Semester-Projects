secure_complaint_system/
│
├── server/
│   ├── server.py              # Main server (socket listener, routing, chat handling)
│   ├── key_manager.py         # KDC logic: long-term keys, session keys, rotation, revocation
│   ├── complaint_manager.py   # Complaint handling, replies, blockchain integration
│   ├── storage.py             # Persistent encrypted storage (users, complaints, replies)
│   ├── logger.py              # Colored logging system (INFO, SUCCESS, ERROR, SECURITY)
│   ├── __init__.py
│
├── client/
│   ├── client.py              # Socket client (auth, complaints, admin ops, live chat)
│   ├── ui.py                  # User/Admin menus (includes Chat menu)
│   ├── crypto_client.py       # Client-side AES encryption utilities
│   ├── __init__.py
│
├── crypto/
│   ├── crypto_utils.py        # AES-CBC, PKCS7 padding, hashing, secrets helpers
│   ├── session_keys.py        # Session key generation + Ephemeral Diffie-Hellman (demo)
│   ├── __init__.py
│
├── data/
│   ├── users.json.enc         # Encrypted user store (long-term keys, roles, status)
│   ├── complaints.json.enc    # Encrypted complaints (persistent storage)
│   ├── replies.json.enc       # Encrypted admin replies
│   ├── blockchain.json        # Blockchain ledger (PoW, plaintext for demonstration)
│   └── logs/
│       └── server.log         # Server-side security & activity logs
│
├── blockchain/
│   ├── blockchain.py          # Block & Blockchain implementation (PoW, nonce, difficulty)
│   ├── __init__.py
│
├── README.md                  # Project overview, security design, usage
│
├── run_server.py              # Starts the secure complaint server
└── run_client.py              # Starts a client instance
