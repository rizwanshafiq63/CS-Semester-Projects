def split_len(plaintext, key_length):
    #return [plaintext[i:i + key_length] for i in range(0, len(plaintext), key_length)]
    result = []
    for i in range(0, len(plaintext), key_length):
        result.append(plaintext[i:i+key_length])
    return result


def encode(plaintext, key):
    #order = {
    #    int(val): num for num, val in enumerate(key)
    #}
    order = {}

    for num, val in enumerate(key):
        order[int(val)] = num

    ciphertext = ""

    for index in sorted(order.keys()):
        for part in split_len(plaintext, len(key)):
            try:
                ciphertext += part[order[index]]

            except IndexError:
                pass

    return ciphertext

plaint = "Hello"
key = "2431"

ciphertxt = encode(plaint, key)

print("Cipher: ", ciphertxt)