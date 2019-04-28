from binascii import unhexlify, b2a_base64
import sys

hex_string = sys.argv[1]

print(b2a_base64(unhexlify(hex_string)))
