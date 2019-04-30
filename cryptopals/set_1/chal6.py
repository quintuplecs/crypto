from itertools import combinations
from base64 import b64decode
import sys, string, base64

letter_frequency = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

CIPHER_TEXT = ''
REGISTERS = {}

def hamming_dist(str1, str2):
    assert (len(str1) == len(str2)), "Lengths of strings must be equal"
    dist = 0

    for bit1, bit2 in zip(str1, str2):
        diff = bin(ord(bit1) ^ ord(bit2))
        dist += diff.count('1')

    return dist

def find_keysize(cipher, answers):
    assert (answers <= len(cipher)), "Number of answers must be less than or equal to the length of the cipher"
    map = {}
    for i in range(2, 50):
        blocks = []
        blocks.append(cipher[:i])
        blocks.append(cipher[i:i*2])
        blocks.append(cipher[i*2:i*3])
        blocks.append(cipher[i*3:i*4])
        block_combinations = tuple(combinations(blocks, 2))
        dist = 0.0
        for str1, str2 in block_combinations:
            dist += hamming_dist(str1, str2)
        dist /= 6.0
        normalized_dist = dist / i
        map[i] = normalized_dist

    sorted_distances = sorted(map, key=map.get)[:answers]
    return sorted_distances

def compute_english_score(str):
    distance = 0.0
    for letter in str:
        distance += letter_frequency.get(letter.lower(), 0)
    return distance

def wrap_text(str, width):
    text = []
    for i in range(0, len(str), width):
        j = i
        block = ''
        while j < len(str) and j < i + width:
            block += str[j]
            j += 1
        text.append(block)
    return text

def transpose(str, key_size):
    wrapped_text = wrap_text(str, key_size)
    transposed_text = []
    for i in range(key_size):
        transposed_text.append(' ')
    for block in wrapped_text:
        for i in range(len(block)):
            transposed_text[i] += block[i]
    return transposed_text

def decrypt_block(block, key):
    result = ''
    key = ord(key)
    for c in block:
        result += chr(ord(c) ^ key)
    return result

def solve_block(block):
    key = ''
    closeness = 0.0
    for i in range(256):
        c = chr(i)
        guess = decrypt_block(block, c)
        value = compute_english_score(guess)
        if value > closeness:
            closeness = value
            key = c
    return key

def guess_keys(cipher, answers):
    key_sizes = find_keysize(cipher, answers)
    possible_keys = []
    for key_size in key_sizes:
        transposed_text = transpose(cipher, key_size)
        key = ''
        for block in transposed_text:
            key += solve_block(block)
        possible_keys.append(key)
    return possible_keys

def decrypt_cipher(cipher, key):
    result = ''
    for i in range(len(cipher)):
        result += chr(ord(cipher[i]) ^ ord(key[i % len(key)]))
    return result

def crack_cipher(cipher, answers = 1):
    keys = guess_keys(cipher, answers)
    dict_score = {}
    dict_text = {}
    for key in keys:
        text = decrypt_cipher(cipher, key)
        score = compute_english_score(text)
        dict_score[key] = score
        dict_text[key] = text
    sorted_dict_score = sorted(dict_score, key=dict_score.get)

    results = []
    for i in range(answers):
        results.append(sorted_dict_score[len(sorted_dict_score) - i - 1])
    chance = {}

    total = sum(value for value in dict_score.values())
    for key in results:
        chance[key] = dict_score[key] / total
    return {
        'keys' : results,
        'scores' : dict_score,
        'text' : dict_text,
        'chance' : chance
    }

def load_file():
    global CIPHER_TEXT, REGISTERS
    print()
    print('Enter file path:')
    path = input()
    try:
        with open(path) as f:
            cipher = b64decode(f.read()).decode('ascii')
    except FileNotFoundError:
        print('Sorry. File not found.')
        return
    CIPHER_TEXT = cipher
    return

def manual_load():
    global CIPHER_TEXT
    print()
    print('Enter the cipher text. Express bytes as usual (EX \\x41):')
    try:
        cipher = input().encode('utf-8').decode('unicode_escape')
    except UnicodeDecodeError:
        print('Error with byte input.')
        return
    CIPHER_TEXT = cipher
    return

def process_crack_cipher():
    global REGISTERS
    print()
    if not CIPHER_TEXT:
        print('No cipher text loaded. Load a file or text first.')
        return
    print('Enter number of keys to search:')
    try:
        selection = int(input())
    except ValueError:
        print('Invalid search space.')
        return
    print('Cipher cracking in progress... (This may take a while for longer cipher texts)')
    try:
        REGISTERS = crack_cipher(CIPHER_TEXT, answers = selection)
    except AssertionError:
        print('Invalid search space.')
        return
    print('Cracking complete.')
    return

def view_keys():
    print()
    header = '-' * 79
    print(header)
    print('{:<5} {:<50} {:<5} {:<5}'.format('ID', 'KEY', 'SCORE', 'CHANCE'))
    print(header)
    for i in range(len(REGISTERS['keys'])):
        print('{:>5} {:<50} {:>6} {:>5}'.format(i, REGISTERS['keys'][i], round(REGISTERS['scores'][REGISTERS['keys'][i]], 1), round(REGISTERS['chance'][REGISTERS['keys'][i]] * 100, 1)))
    print(header)
    return

def view_decrypted_cipher():
    print()
    print('Enter id of key:')
    try:
        key = int(input())
    except ValueError:
        print('Invalid key id.')
        return
    try:
        text = REGISTERS['text'][REGISTERS['keys'][key]]
    except IndexError:
        print('Invalid key id.')
        return
    print('-------------BEGIN DECODED MESSAGE----------------')
    print(text)
    print('--------------END DECODED MESSAGE-----------------')
    return

def view_registers():
    if not REGISTERS:
        print('Registers not loaded. Crack a cipher first.')
        return
    while 1:
        print()
        print('Register Selection')
        print('1: Cipher text')
        print('2: Keys')
        print('3: Decrypted cipher')
        print('4: Exit')
        try:
            selection = int(input())
        except ValueError:
            print('Invalid selection.')
            continue
        if selection < 1 or selection > 5:
            print('Invalid selection.')
            continue
        elif selection == 1:
            print(CIPHER_TEXT)
        elif selection == 2:
            view_keys()
        elif selection == 3:
            view_decrypted_cipher()
        elif selection == 4:
            print()
            break

def help_menu():
    print()
    print('Menu options')
    print()
    print('Load file:')
    print('Enter the path of where the file is. Make sure the contents of the file are in base 64.')
    print('This function takes the file contents, decodes the base 64, and derives the cipher from')
    print('the encoded file.')
    print()
    print('Manual load:')
    print('Manually enter string that is the cipher. Bytes can be expressed per normal python')
    print('syntax.')
    print()
    print('Crack cipher:')
    print('After the cipher is loaded, call this function to crack it and the results will be sent')
    print('to the registers.')
    print()
    print('View registers')
    print('This function prints the results of the cipher cracking in pretty print. You can see the')
    print('original ciphertext, the cracked keys and their associated probabilities, as well as the')
    print('decoded ciphertext.')
    return

def main():
    print('\    /   -----     -----')
    print(' \  /   |     |   |     |')
    print('  \/    |     |    -----')
    print('  /\    |     |   |   \ ')
    print(' /  \   |     |   |    \ ')
    print('/    \   -----    |     |')
    print('9fh9#$1jf#CRACKERF59j3$18hf#')
    print()
    while 1:
        print()
        print('MENU')
        print('1: Load file')
        print('2: Manual load')
        print('3: Crack cipher')
        print('4: View registers')
        print('5: Help')
        print('6: Quit')
        try:
            selection = int(input())
        except ValueError:
            print('Not a valid selection.')
            continue
        if selection > 6 or selection < 1:
            print('Not a valid selection.')
            continue
        elif selection == 1:
            load_file()
        elif selection == 2:
            manual_load()
        elif selection == 3:
            process_crack_cipher()
        elif selection == 4:
            view_registers()
        elif selection == 5:
            help_menu()
        elif selection == 6:
            print()
            print('Goodbye.')
            break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print('Goodbye.')
