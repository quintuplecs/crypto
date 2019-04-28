import sys
import operator

def get_str(m):
    last_digit = m % 10
    if last_digit == 1:
        return 'st'
    elif last_digit == 2:
        return 'nd'
    elif last_digit == 3:
        return 'rd'
    else:
        return 'th'

hex_string = sys.argv[1]
n = int(sys.argv[2])
dict = {}

for i in range(0, len(hex_string), 2):
    byte = hex_string[i] + hex_string[i + 1]
    if byte in dict:
        dict[byte] += 1
    else:
        dict[byte] = 1

sorted_dict = sorted(dict.items(), key = lambda kv:(kv[1], kv[0]))

for i in range(n):
    print('{}{} most common byte: 0x{}'.format(i + 1, get_str(i + 1), sorted_dict[len(sorted_dict) - i - 1][0]))
    print('Occurence: {}'.format(sorted_dict[len(sorted_dict) - i - 1][1]))
    print()
