from pwn import *
from binascii import unhexlify
import sys

def extract(filename):
    e = ELF(filename)

    # Disassemble the entrypoint and find the address of the main function
    entry_addr =  e.entry # 0x10c0
    entry_asm = e.disasm(entry_addr, 30)
    # 10d4:       48 8d 3d 32 01 00 00    lea    rdi, [rip+0x132]             # 0x120d
    offset = 0x14 # from start of entry
    main_addr = int(e.disasm(entry_addr + offset, 7).split('# ')[1], 16) # 0x120d

    try:
        # Disassemble the main function and find the adresses we want
        # 12e8:       48 8d 15 71 2d 00 00    lea    rdx, [rip+0x2d71]             # 0x4060    // offset
        # 12f8:       8b 0d fe df 18 00       mov    ecx, DWORD PTR [rip+0x18dffe] # 0x18f2fc  // offset+0x10
        # 1309:       48 8d 05 d0 db 18 00    lea    rax, [rip+0x18dbd0]           # 0x18eee0  // offset+0x21
        # 133b:       8b 05 87 db 18 00       mov    eax, DWORD PTR [rip+0x18db87] # 0x18eec8  // offset+0x53
        if filename == "introspection":
            offset = 0xdB
        else:
            offset = 0xc5
        data1_addr = int(e.disasm(main_addr + offset, 7).split('# ')[1], 16) # 0x4060
        len2_addr  = int(e.disasm(main_addr + offset + 0x10, 6).split('# ')[1], 16) # 0x18f2fc
        data2_addr = int(e.disasm(main_addr + offset + 0x21, 7).split('# ')[1], 16) # 0x18eee0
        len1_addr  = int(e.disasm(main_addr + offset + 0x53, 6).split('# ')[1], 16) # 0x18eec8

        # Read the data at these adresses
        len1  = unpack(e.read(len1_addr, 4))
        len2  = unpack(e.read(len2_addr, 4))
        data1 = e.read(data1_addr, len1)
        data2 = e.read(data2_addr, len2)
        return data1, len1, data2, len2
    except:
        exit()


def mimic(data1, len1, data2, len2):
    lVar5 = 0
    lVar6 = -1
    data1 = list(data1)
    for i in range(len1):
        data1[i] = lVar6 + lVar5 + data2[i % len2] + 1^data1[i]
    return bytes(data1)

def store(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

elf = "introspection"
count = 0
while True:
    count += 1
    extracted = "extracted" + str(count)
    data1, len1, data2, len2 = extract(elf)
    store(extracted, mimic(data1, len1, data2, len2))
    print("Inception level ", count)
    elf = extracted

