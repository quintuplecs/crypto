from chal10 import cbc_encrypt, ecb_encrypt
from secrets import token_bytes
from random import randint
from Crypto.Cipher.AES import block_size

ECB = True
CBC = False

def random_key():
    return token_bytes(16)

def obfuscate_plaintext(plaintext):
    return token_bytes(randint(5, 11)) + plaintext + token_bytes(randint(5, 11))

def encryption_oracle(plaintext):
    selection = randint(0, 2)
    plaintext = obfuscate_plaintext(plaintext)
    if selection == 0:
        return ecb_encrypt(plaintext, random_key()), ECB
    else:
        return cbc_encrypt(plaintext, random_key(), random_key()), CBC

def detect_ecb(ciphertext):
    blocks = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
    return CBC if len(blocks) == len(set(blocks)) else ECB

# Essentially the ECB detector doesn't work with plaintext that have a short length, as there
# won't be any duplicate blocks. However, the longer the plaintext is, the more likely there
# is to be repeating text. This code scores around 800-850 correct out of 1000 test cases with
# the test data I made. However, that number drops to < 400 correct when you feed it a normal
# English sentence.

def main():
    with open('data/chal11_test_data') as f:
        plaintext = f.read().encode()
    correct = 0
    for i in range(1000):
        ciphertext, encryption_type = encryption_oracle(plaintext)
        correct += 1 if encryption_type == detect_ecb(ciphertext) else -1
    print(correct)

if __name__ == '__main__':
    main()
