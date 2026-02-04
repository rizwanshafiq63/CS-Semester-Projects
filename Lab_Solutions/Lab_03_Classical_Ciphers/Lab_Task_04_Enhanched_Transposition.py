import random

# ----------------------------
# Utility: split into chunks
# ----------------------------
def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]

# ----------------------------
# 1. Handle Different Key Sizes + Padding
# ----------------------------
def pad_plaintext(plaintext, key_len):
    padding_char = "_"
    extra = len(plaintext) % key_len
    if extra != 0:
        plaintext += padding_char * (key_len - extra)
    return plaintext

# ----------------------------
# Encode function
# ----------------------------
def encode(key, plaintext):
    key_len = len(key)
    plaintext = pad_plaintext(plaintext, key_len)

    order = {int(val): num for num, val in enumerate(key)}
    ciphertext = ''

    for index in sorted(order.keys()):
        for part in split_len(plaintext, key_len):
            try:
                ciphertext += part[order[index]]
            except IndexError:
                pass
    return ciphertext

# ----------------------------
# 2. Decode function
# ----------------------------
def decode(key, ciphertext):
    key_len = len(key)
    order = {int(val): num for num, val in enumerate(key)}

    # Number of rows
    num_rows = len(ciphertext) // key_len

    # Build empty matrix
    table = [[""] * key_len for _ in range(num_rows)]

    k = 0
    for index in sorted(order.keys()):
        col = order[index]
        for row in range(num_rows):
            table[row][col] = ciphertext[k]
            k += 1

    # Flatten back to plaintext
    plaintext = "".join("".join(row) for row in table)
    return plaintext.rstrip("_")  # remove padding

# ----------------------------
# 3 + 4. Preserve case, spaces & punctuation
#    (already preserved, since we don’t lower())
# ----------------------------

# ----------------------------
# 5. Dynamic Key Generation
# ----------------------------
def generate_key(length):
    if length > 9:
        length = 9  # limit key size
    digits = list(range(1, length + 1))
    random.shuffle(digits)
    return "".join(map(str, digits))
# def generate_key(length):
#     digits = list(range(1, length + 1))
#     random.shuffle(digits)
#     return "".join(map(str, digits))

# ----------------------------
# 6. Menu Interface
# ----------------------------
def menu():
    while True:
        print("\n--- Transposition Cipher Menu ---")
        print("1. Encode a message")
        print("2. Decode a message")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            plaintext = input("Enter plaintext: ")
            key = input("Enter key (or press Enter to auto-generate): ")
            if not key:
                key = generate_key(len(plaintext))
                print(f"Generated Key: {key}")

            ciphertext = encode(key, plaintext)
            print("Ciphertext:", ciphertext)

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            key = input("Enter key: ")
            plaintext = decode(key, ciphertext)
            print("Plaintext:", plaintext)

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

# ----------------------------
# Run the menu
# ----------------------------
if __name__ == "__main__":
    menu()
