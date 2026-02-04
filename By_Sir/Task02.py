import random

# split string into chunks
def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


# Encode function
def encode(key, plaintext):
    # Padding if needed
    while len(plaintext) % len(key) != 0:
        plaintext += "_"

    n = len(key)
    rows = split_len(plaintext, n)

    # Generate column order based on key digits
    order = sorted([(int(k), i) for i, k in enumerate(key)])

    ciphertext = ""
    for _, col_index in order:  # read by key order
        for row in rows:
            ciphertext += row[col_index]
    return ciphertext


# Decode function
def decode(key, ciphertext):
    n = len(key)
    rows_count = len(ciphertext) // n

    order = sorted([(int(k), i) for i, k in enumerate(key)])

    # Split ciphertext into column chunks
    cols = {}
    k = 0
    for _, col_index in order:
        cols[col_index] = ciphertext[k:k + rows_count]
        k += rows_count

    # Reconstruct plaintext row by row
    plaintext = ""
    for i in range(rows_count):
        for j in range(n):
            plaintext += cols[j][i]

    return plaintext.replace("_", "")


# Random key generator
def generate_key(length):
    digits = list(range(1, length + 1))
    random.shuffle(digits)
    return "".join(str(d) for d in digits)


# Menu system
def menu():
    while True:
        print("\n--- Transposition Cipher ---")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            plaintext = input("Enter plaintext: ")
            key = input("Enter key (leave empty for auto-generate): ")
            if not key:
                key = generate_key(len(plaintext))
                print("Randomly generated key:", key)
            ciphertext = encode(key, plaintext)
            print("Ciphertext:", ciphertext)

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            key = input("Enter key: ")
            plaintext = decode(key, ciphertext)
            print("Plaintext:", plaintext)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


# Run program
if __name__ == "__main__":
    menu()