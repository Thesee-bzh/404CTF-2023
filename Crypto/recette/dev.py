from binascii import unhexlify
import re

with open("sequence.txt", "r") as f:
    seq = f.readline().strip(); print('sequence', seq, '\n')
    seq = unhexlify(seq).decode(); print('unhexlify', seq, '\n')
    # Develop so that we don't have any digits
    dev = ''
    for op in re.split('([0-9]+[isdo])', seq):
        if op != '':
            # Example: 15i => cnt = 15, ins = 'i'
            cnt = op[:-1]
            ins = op[-1:]
            dev += ins * int(cnt) 
    print('developped', dev, '\n')
