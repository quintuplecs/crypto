def pad(text, block_size):
    assert len(text) < block_size
    padding_length = block_size - len(text)
    padded_text = text + (chr(padding_length) * padding_length)
    return padded_text

def main():
    print(pad('YELLOW SUBMARINE', 20).encode())

if __name__ == '__main__':
    main()
