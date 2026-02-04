# Task05 — Q5. Bit-Flipping Experiment (AES-CBC vs DES-CBC)

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def flip_one_bit(b: bytes, index: int = 0, bit: int = 0) -> bytes:
    x = bytearray(b); x[index] ^= (1 << bit); return bytes(x)

def count_byte_diffs(a: bytes, b: bytes) -> int:
    n = min(len(a), len(b))
    return sum(1 for i in range(n) if a[i] != b[i]) + abs(len(a) - len(b))

def run(name, cipher_cls, block_size, key_len, iv_len, msg: bytes):
    key = get_random_bytes(key_len)
    iv  = get_random_bytes(iv_len)

    ct  = cipher_cls.new(key, cipher_cls.MODE_CBC, iv=iv).encrypt(pkcs7_pad(msg, block_size))
    ct_flipped = flip_one_bit(ct, 0, 0)  # flip 1 bit in the very first byte

    dec_simple  = cipher_cls.new(key, cipher_cls.MODE_CBC, iv=iv).decrypt(ct)
    dec_flipped = cipher_cls.new(key, cipher_cls.MODE_CBC, iv=iv).decrypt(ct_flipped)

    total_changed = count_byte_diffs(dec_simple, dec_flipped)
    b = block_size
    first_block_changed  = count_byte_diffs(dec_simple[:b],    dec_flipped[:b])

    print(f"\n=== {name}-CBC (block={block_size}) ===")
    print("Key:", key.hex())
    print("IV :", iv.hex())
    print("Ciphertext:", ct.hex())
    print("Ciphertext (1-bit flipped):", ct_flipped.hex())
    print(f"Bytes changed in 1st block: {first_block_changed} / {block_size}")

    if len(dec_simple) >= 2*b:
        second_block_changed = count_byte_diffs(dec_simple[b:2*b], dec_flipped[b:2*b])
        print(f"Bytes changed in 2nd block: {second_block_changed} / {block_size}")
    else:
        print("Only one block after padding → next-block flip not visible for this message.")

    print(f"Bytes changed overall:      {total_changed} / {len(dec_simple)}")

if __name__ == "__main__":
    text = input("Enter a short message (default used if empty): ").strip() or "This is task05 answer!"
    msg = text.encode("utf-8")

    # AES: 16-byte block; DES: 8-byte block
    run("AES", AES, 16, 16, 16, msg)
    run("DES", DES,  8,  8,  8,  msg)

    print("\nExplanation (4–5 lines):")
    print("- In CBC mode, each block depends on the previous ciphertext block.")
    print("- If one bit of ciphertext changes, the whole block after decryption becomes random.")
    print("- The same bit also flips in the next block because of the XOR step in CBC.")
    print("- AES uses bigger blocks (16 bytes) than DES (8 bytes), so the error spreads over more bytes.")

