import sys

hex_string1 = sys.argv[1]
hex_string2 = sys.argv[2]

xor_result = int(hex_string1, 16) ^ int(hex_string2, 16)

print(hex(xor_result)[2:])
