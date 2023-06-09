# Retro / L'inspiration en images

## Challenge
Un quart d'heure plus tôt dans la soirée, vous étiez en train de parler avec Sabine de vos méthodes créatives, de vos exercices de style dans vos mediums respectifs. Elle mentionna au fil de la conversation son atelier de peinture se situant dans les combles rustiques du café littéraire, vous suggérant que vous pourriez toujours prendre de l'inspiration en observant ses peintures, son processus de création, sa manière de capturer la beauté insaisissable.

Une fois la conversation et le café terminés, vous vous aventurez dans l'atelier de peinture de Sabine, votre lampe torche à la main. Au milieu de cette mer de tableaux, vous repérez une peinture étrange, criblée d'inscriptions.

Et au pied du chevalet a chu une note, sur laquelle il est marqué : 'Ma clé est la couleur du fond de la toile'. Vous remarquez également d'autres inscriptions incompréhensibles au verso de la note. Sans doute un message chiffré ?

Vous vous mettez en quête de la clé.

> Note : Le déchiffrage du message n'est pas nécessaire à la complétion du challenge.

> Format : 404CTF{vec4(r,g,b,a)} où r,g,b et a sont des flottants précis au dixième.

## Inputs
- binary: [vue_sur_un_etrange_tableau](./vue_sur_un_etrange_tableau)


## Solution
Disassembling the binary in `Ghidra` shows an `OpenGL` application. Googling around how to set the background color leads to function `glad_glClearColor()`, which we can find in a single location in the `main()` function:

```c
(*glad_glClearColor)(0x3e4ccccd,0x3e99999a,0x3e99999a,0x3f800000);
```

So this gives us the `RGBA` values, which are converted from hex to float in python as follow:

```python
from binascii import unhexlify
import struct

rgba = ['0x3e4ccccd','0x3e99999a','0x3e99999a','0x3f800000']

for color in rgba:
    print(struct.unpack('>f', unhexlify(color[2:])))
```

```console
$ python3 sol.py
(0.20000000298023224,)
(0.30000001192092896,)
(0.30000001192092896,)
(1.0,)
```

We just need to round to the first decimal to get the flag.

## Flag

404CTF{vec4(0.2,0.3,0.3,1.0)}
