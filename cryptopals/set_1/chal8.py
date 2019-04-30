from Crypto.Cipher.AES import block_size
from binascii import unhexlify

def find_duplicates(cipher_text):
    chunks = [cipher_text[i : i + block_size] for i in range(0, len(cipher_text), block_size)]
    duplicates = len(chunks) - len(set(chunks))
    return duplicates

def main():
    duplicates = []
    with open('data/chal8') as f:
        for line in f:
            str = unhexlify(line[:len(line)-1])
            duplicates.append(find_duplicates(str))
    print(max(duplicates))

if __name__ == '__main__':
    main()
