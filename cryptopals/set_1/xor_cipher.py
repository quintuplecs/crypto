from binascii import unhexlify
import sys

c = sys.argv[1]
k = sys.argv[2]

result = ''
for i in range(len(c)):
    result += chr(ord(c[i]) ^ ord(k[i % len(k)]))

print(result)
