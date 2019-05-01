from chal9 import pad, unpad
from Crypto.Cipher import AES
from base64 import b64decode

def ecb_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, 16))

def ecb_decrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(plaintext)

def xor(plaintext, key):
    result = b''
    for i in range(len(plaintext)):
        result += chr(plaintext[i] ^ key[i % len(key)]).encode()
    return result

def cbc_encrypt(plaintext, key, iv):
    result = b''
    ciphertext = iv
    for i in range(0, len(plaintext), AES.block_size):
        xor_result = xor(plaintext[i : i + AES.block_size], ciphertext)
        ciphertext = ecb_encrypt(xor_result, key)
        result += ciphertext
    return result

def cbc_decrypt(ciphertext, key, iv):
    result = b''
    xor_key = iv
    for i in range(0, len(ciphertext), AES.block_size):
        block = ciphertext[i : i + AES.block_size]
        ecb_result = ecb_decrypt(block, key)
        result += xor(ecb_result, xor_key)
        xor_key = block
    return unpad(result)

def main():
    with open('data/chal10') as f:
        ciphertext = b64decode(f.read())
    print(cbc_decrypt(ciphertext, b'YELLOW SUBMARINE', b'\x00').decode('ascii'))

if __name__ == '__main__':
    main()
