from Crypto.Cipher import AES
from base64 import b64decode

key = b'YELLOW SUBMARINE'

with open('data/aes_ciphertext') as f:
    cipher_text = b64decode(f.read())

cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(cipher_text).decode('ascii'))
