from pwn import *

c = remote('challenges.404ctf.fr', 31420)

# Grab the all output
flood = c.recvuntil(b'> '); print(flood.decode())

# Count rhinos
while True:
    # Count rhinos and send response
    rhino = '~c`°^)'
    count = flood.decode().count(rhino)
    c.send(str(count).encode() + b'\n'); print(count, '\n')
    # Next
    line = c.recvline(); print(line.decode())
    if b"la suite arrive !" in line:
        try:
            flood = c.recvuntil(b'> '); print(flood.decode())
        except:
            break

# Finished counting rhinos, dump the end and look for flag
while b'404CTF' not in line:
    line = c.recvline(); print(line.decode())

# Vous faites exactement cela, à l'intérieur se trouve un billet, et une lettre. Dessus il est marqué 404CTF{4h,_l3s_P0uvo1rs_d3_l'iNforM4tiqu3!}
