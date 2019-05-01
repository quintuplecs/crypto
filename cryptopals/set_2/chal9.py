def pad(text, block_size):
    partition = text[:len(text) % block_size]
    padding_length = block_size - len(partition)
    padded_text = text + (chr(padding_length) * padding_length).encode()
    return padded_text

def unpad(text):
    return text[:len(text) - ord(text[-1:])]

def main():
    print(pad('YELLOW SUBMARINE', 20).encode())

if __name__ == '__main__':
    main()
