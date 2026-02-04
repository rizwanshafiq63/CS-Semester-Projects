# Task01 — AES 

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# --- PKCS7 padding helpers ---
def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes, block_size: int = 16) -> bytes:
    if not padded or len(padded) % block_size != 0:
        raise ValueError("Invalid padded data length")
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len]

# --- Caesar cipher (shift = 3) ---
def caesar_shift(text: str, shift: int = 3) -> str:
    res = []
    for ch in text:
        if 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(ch)  
    return ''.join(res)

def main():
    plaintext = input("Enter plaintext: ")
    # Step 2: Caesar
    caesar_out = caesar_shift(plaintext, 3)
    print(f"Caesar output: {caesar_out}")

    # Step 3: AES-CBC
    key = get_random_bytes(16)         # 128-bit AES key
    iv = get_random_bytes(16)          # 16-byte IV for CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    padded = pkcs7_pad(caesar_out.encode('utf-8'), 16)
    ct = cipher.encrypt(padded)

    print(f"AES key (hex): {key.hex()}")
    print(f"IV      (hex): {iv.hex()}")
    print(f"Ciphertext (base64): {base64.b64encode(ct).decode()}")

    # Step 4: Decrypt & verify
    decipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = decipher.decrypt(ct)
    decrypted_text = pkcs7_unpad(decrypted_padded, 16).decode('utf-8')
    print(f"Decrypted after AES: {decrypted_text}")
    # Reverse Caesar to verify original
    recovered = caesar_shift(decrypted_text, -3)
    print(f"Recovered plaintext (after reverse Caesar): {recovered}")
    print("Match with original?", recovered == plaintext)

if __name__ == "__main__":
    main()