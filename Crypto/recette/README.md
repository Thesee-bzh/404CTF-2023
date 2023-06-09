# Crypto / Recette

## Challenge
Le Commissaire Maigret, café à la main, vous raconte une de ses dernières enquêtes. Il vous explique que sur une scène de crime il a retrouvé un papier faisant office de message codé. Il le sort de sa poche pour vous le montrer :

- Convertir depuis l'hexadécimal
- Développer de sorte à ne plus voir de chiffres
- Décoder le DeadFish
- Convertir depuis la Base 85


## Inputs
Sequence: 32 69 31 73 34 69 31 73 31 35 64 31 6f 34 39 69 31 6f 34 64 31 6f 33 69 31 6f 31 35 64 31 6f 32 32 64 31 6f 32 30 64 31 6f 31 39 69 31 6f 37 64 31 6f 35 64 31 6f 32 69 31 6f 35 35 69 31 6f 31 64 31 6f 31 39 64 31 6f 31 37 64 31 6f 31 38 64 31 6f 32 39 69 31 6f 31 32 69 31 6f 32 36 69 31 6f 38 64 31 6f 35 39 64 31 6f 32 37 69 31 6f 36 64 31 6f 31 37 69 31 6f 31 32 64 31 6f 37 64 31 6f 35 69 31 6f 31 64 31 6f 32 64 31 6f 31 32 69 31 6f 39 64 31 6f 32 36 64 31 6f


## Solution
Let's write some python code to `unhexlify` and develop the input sequence:

```python
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
```

Here's the output:
```console
$ python3 dev.py
sequence 3269317334693173313564316f343969316f3464316f3369316f313564316f323264316f323064316f313969316f3764316f3564316f3269316f353569316f3164316f313964316f313764316f313864316f323969316f313269316f323669316f3864316f353964316f323769316f3664316f313769316f313264316f3764316f3569316f3164316f3264316f313269316f3964316f323664316f

unhexlify 2i1s4i1s15d1o49i1o4d1o3i1o15d1o22d1o20d1o19i1o7d1o5d1o2i1o55i1o1d1o19d1o17d1o18d1o29i1o12i1o26i1o8d1o59d1o27i1o6d1o17i1o12d1o7d1o5i1o1d1o2d1o12i1o9d1o26d1o

developped iisiiiisdddddddddddddddoiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiioddddoiiiodddddddddddddddoddddddddddddddddddddddoddddddddddddddddddddoiiiiiiiiiiiiiiiiiiiodddddddodddddoiioiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiododddddddddddddddddddodddddddddddddddddoddddddddddddddddddoiiiiiiiiiiiiiiiiiiiiiiiiiiiiioiiiiiiiiiiiioiiiiiiiiiiiiiiiiiiiiiiiiiioddddddddodddddddddddddddddddddddddddddddddddddddddddddddddddddddddddoiiiiiiiiiiiiiiiiiiiiiiiiiiioddddddoiiiiiiiiiiiiiiiiioddddddddddddodddddddoiiiiiododdoiiiiiiiiiiiiodddddddddoddddddddddddddddddddddddddo
```

This is indeed some `deadfish` code, which decodes into `1b^aR<(;4/1hgTC1NZtl1LFWKDIHFRI/` using https://www.dcode.fr/deadfish-language, which then decodes into `404CTF{M4igr3t_D3_c4naRd}` using `CyberChef` (From Base85).

## Python code
Solution to unhexlify & delevop in [dev.py](./dev.py)

## Flag
404CTF{M4igr3t_D3_c4naRd}

