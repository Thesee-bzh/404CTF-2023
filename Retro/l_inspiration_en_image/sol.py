from binascii import unhexlify
import struct

rgba = ['0x3e4ccccd','0x3e99999a','0x3e99999a','0x3f800000']

for color in rgba:
    print(struct.unpack('>f', unhexlify(color[2:])))
