# Crypto / Dessine-moi une courbe elliptique

## Challenge
Au cours d'une de vos explorations dans le café, vous surprenez la conversation suivante :

Oh ! Ce jour, je m'en souviens parfaitement, comme si c'était hier. À cette époque, je passais mes journées à mon bureau chez moi, avec comme seule occupation de dessiner les illustrations qui m'étaient commandées par les journaux du coin. Je ne m'en rendais pas compte à ce moment, mais cela faisait bien 6 ans que je vivais cette vie monacale sans réelle interaction humaine. Le temps passe vite quand on n'a rien à faire de ses journées. Mais ce jour-là, c'était différent. Je m'apprêtais à commencer ma journée de travail, un peu stressé parce que j'avais des illustrations que je devais absolument finir aujourd'hui. Alors que je venais de m'installer devant ma planche à dessin, quelle ne fut pas ma surprise d'entendre une voix venir de derrière-moi :
« S'il-te plaît, dessine moi une courbe elliptique. »
Je me suis retourné immédiatement. Un petit bonhomme se tenait derrière moi, dans mon appartement, habillé de façon tout à fait incongrue. Il portait une sorte de tenue de mousquetaire céleste ? Même aujourd'hui je ne sais toujours pas comment la décrire.

« Quoi ?

— S'il-te plaît, dessine moi une courbe elliptique. »

Devant cette situation ubuesque, mon cerveau a lâché, a abandonné. Je ne cherchais plus à comprendre et je me contentais de répondre:

« Je ne sais pas ce que c'est.

— Ce n'est pas grave, je suis sûr que tu pourras en dessiner une belle! Répondit l'enfant en rigolant. »

Machinalement, je pris mon crayon, et je dessinai à main levée une courbe, sans réfléchir. Après quelques instants, je me suis retourné, et j'ai montré le résultat à l'enfant, qui secoua immédiatement la tête.

« Non, regarde: cette courbe à un déterminant nul, je ne veux pas d'une courbe malade ! »

À ce moment, je ne cherchais plus à comprendre ce qu'il se passait. J'ai donc fait la seule chose que je pouvais faire, j'en ai redessiné une. Cette fois, l'enfant était très heureux.

« Elle est magnifique ! Je suis sûr qu'elle sera très heureuse toute seule. »

Et là, sous mes yeux ébahis, la courbe pris vie depuis mon dessin, et s'envola dans la pièce. Elle se mit à tourner partout, avant de disparaître. J'étais bouche bée, enfin encore plus qu'avant.

« Ah, elle avait envie de bouger visiblement !

— Où est-elle partie ?

— Je ne sais pas. Mais c'est toi qui l'a dessinée ! Tu ne devrais pas avoir de mal à la retrouver. En plus je crois qu'elle t'a laissé un petit souvenir, dit-il en pointant le sol, où une série de chiffres étaient effectivement dessinés sur le parquet.

— Merci encore ! Sur ce, je dois partir. Au revoir ! »

Avant que je puisse ouvrir la bouche, il disparût.
Je ne sais toujours pas ce qu'il s'est passé ce jour-là, mais je retrouverais cette courbe un jour !


Peut-être pourriez-vous l'aider ?

## Inputs
- python challenge: [challenge.py](./challenge.py)
- dumped output: [data.txt](./data.txt)


## Solution
The line `determinant = 4 * a**3 + 27 * b**2` tells us `(a, b)` are the parameters of the elliptic curve with the Weirstrass form `y^2 = x^3 + ax + b mod p`. We know Two points on this curve and the modulus (from `data.txt`). This is enough to recover `(a, b)`.

See this post for an explanation:

> https://crypto.stackexchange.com/questions/97811/find-elliptic-curve-parameters-a-and-b-given-two-points-on-the-curve

Let's `(x1, y1)` and `(x2, y2)` be the coordinates of the two points logged in `data.txt`. Then we have two equations with two variables:

- y1^2 = x1^3 + ax1 + b mod p
- y2^2 = x2^3 + ax2 + b mod p

Let's substract both equations to eliminate `b`:

- y1^2 - y1^2 = x1^3 - x2^3 + ax1 - ax2 mod p
- (y1^2 - y1^2) - (x1^3 - x2^3) = a(x1 - x2) mod p
- ((y1^2 - y1^2) - (x1^3 - x2^3)) * (x1 - x2)^-1 = a mod p

To be able to find `a`, the only problem is the existence of the modular inverse of `(x1−x2)` modulo `p`. But we have `gcd((x1 - x2), n) = 1`, so the inverse does exist. Then `b` is easily recovered with:

- b = (y1^2 - x1^3) - ax1

Let's implement it in `python/sage`:

```python
from sage.all import *

p = 231933770389389338159753408142515592951889415487365399671635245679612352781

# Two points on the curve, from data.txt
x1 = 93808707311515764328749048019429156823177018815962831703088729905542530725
y1 = 144188081159786866301184058966215079553216226588404139826447829786378964579
x2 = 139273587750511132949199077353388298279458715287916158719683257616077625421
y2 = 30737261732951428402751520492138972590770609126561688808936331585804316784

# https://crypto.stackexchange.com/questions/97811/find-elliptic-curve-parameters-a-and-b-given-two-points-on-the-curve
# To be able to find a the only problem is the existence of the modular multiplicative inverse of (x1−x2) mod p.
# a = [(y1^2-y2^2)-(x1^3-x2^3)](x1-x2)^-1 mod p; b = (y1^2-x1^3)-ax1
Zp = IntegerModRing(p)
x = Zp(x1-x2)
y = Zp((y1**2 - y2**2) - (x1**3 - x2**3))
a = Zp(((y1**2 - y2**2) - (x1**3 - x2**3)) * (x**-1))
b = Zp(y1**2 - x1**3 - a*x1)
print(a, b)
```

```console
$ python3 sol.sage
14902775479549176103916693271068277706052934716440896707334978512750519253 220048944991955967308525489300590382240260882141745561912602020777012600739
```

Now we have `(a, b)`, so we elliptic curve is known.

Then, from the `challenge.py`, the flag is `AES`-encrypted with the `key` equal to the concatenation of `a` and `b`:

```python
iv = urandom(16)
key = str(a) + str(b)
aes = AES.new(hashlib.sha1(key.encode()).digest()[:16], AES.MODE_CBC, iv=iv)
cipher = aes.encrypt(FLAG)
print(cipher.hex())
print(iv.hex())
```

Since we know `(a, b)`, we know the `key`. The `iv` is also logged in `data.txt`, so the decryption is easy:

```python
# Cipher and IV, from data.txt
cipher = unhexlify('8233d04a29befd2efb932b4dbac8d41869e13ecba7e5f13d48128ddd74ea0c7085b4ff402326870313e2f1dfbc9de3f96225ffbe58a87e687665b7d45a41ac22')
iv = unhexlify('00b7822a196b00795078b69fcd91280d')

# Decrypt
key = str(a) + str(b)
aes = AES.new(hashlib.sha1(key.encode()).digest()[:16], AES.MODE_CBC, iv=iv)
flag = aes.decrypt(cipher)
print(flag.decode())
```

```console
$ python3 sol.sage
404CTF{70u735_l35_gr4nd35_p3r50nn3s_0nt_d_@b0rd_373_d35_3nf4n7s}
```

## python code
Complete solution in [sol.sage](./sol.sage)

## Flag
404CTF{70u735_l35_gr4nd35_p3r50nn3s_0nt_d_@b0rd_373_d35_3nf4n7s}
