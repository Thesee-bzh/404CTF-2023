# Crypto / La réponse de Voris

## Challenge
Vous rencontrez Mme de Beauvoir qui vous explique vouloir surprendre son mari Jean Sol Partre. Ce dernier est en train d'écrire un livre et a demandé à son ami Voris un titre approprié. Elle a réussi à se procurer un étrange message, qu'elle pense avoir été chiffré par Voris afin de limiter les fuites d'information. Ne sachant quoi faire avec ceci, elle s'est décidée à aller à la séance de spiritualisme du samedi au café littéraire, où elle vous a rencontré aujourd'hui. Par chance, vous connaissez une oracle pouvant peut être vous aider à déchiffrer ce message. Mais, malchance, cette dernière n'est qu'en mesure de chiffrer un message... Dommage, il va falloir réfléchir pour trouver le titre que Voris a proposé à Jean Sol !

> Format : 404CTF{titre_du_livre}

## Inputs
- server at challenges.404ctf.fr:31682
- ciphered message : pvfdhtuwgbpxfhocidqcznupamzsezp

## Solution
Explicit reference to `L'écume des jours` from `Boris Vian`, starring `Jean-Paul Sartre` as `Jean-Sol Partre`.

It's about the same thing as in the challenge `Le jour de l'espace`. But here, the input message is not encoded by blocks: an input message of length `n` gets encrypted with output lenght `n`.

```console
$ nc challenges.404ctf.fr 31682
Bienvenue dans loracle, qui chiffre ce que vous rentrez. Vous devez dechiffrer : pvfdhtuwgbpxfhocidqcznupamzsezp
message en clair : a
message chiffre  : c

message en clair : aa
message chiffre  : qf

message en clair : qq
message chiffre  : wb

message en clair : asdc
message chiffre  : nysg
```

We'll adopt the same method as in `Le journal de l'espace`, starting with `a`*31 (the length of the message to decode), then changing one letter at a time and see the effect on the output:

```console
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa gvshnmijdwalablggmejiqvrhkixhns
baaaaaaaaaaaaaaaaaaaaaaaaaaaaaa hxvlssprmglxnpawxexddmspgkjzkrx
caaaaaaaaaaaaaaaaaaaaaaaaaaaaaa izypxywzvqwjadpmowqxyipnfkkbnvc
daaaaaaaaaaaaaaaaaaaaaaaaaaaaaa jbbtcedheahvnrecfojrtemlekldqzh
eaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa kdexhkkpnkshaftswgcloajjdkmftdm
faaaaaaaaaaaaaaaaaaaaaaaaaaaaaa lfhbmqrxwudtntiinyvfjwghcknhwhr
gaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa mhkfrwyffeofahxyeqozesdfbkojzlw
(...)
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaav bqncihdeyrvgvwgbbhzedlqmcfdscin
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaw crodjiefzswhwxhcciafemrndgetdjo
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaax dspekjfgatxixyiddjbgfnsoehfuekp
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaay etqflkghbuyjyzjeekchgotpfigvflq
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaz furgmlhicvzkzakffldihpuqgjhwgmr
```

Again, we assume a `linear transform` and compute the corresponding  `matrix A`. To identify this matrix, we need to compute all coefficients `ai,j`, which describe how character `i` in the input affects character `j` in the output.

The code is the same as in `Le jour de l'espace` (except letter `z` is valid now, so everything is `modulo 26` now).

```python
def get_transform(clist, size):
    dlist = list()
    # loop on characters in block
    for i in range(0, size):
        # loop on encrypted blocks
        for j in range(len(clist)-1):
            w1 = clist[j]; w2 = clist[j+1]
            diff = (ord(w2[i]) - ord(w1[i])) % 26
            # Make sure we have a constant difference
            if j != 0 and diff != delta:
                assert()
            delta = diff
        dlist.append(delta)
    return(dlist)

def get_transfrom_matrix(clist, size):
    m = list()
    for l in clist:
        t = get_transform(l, size)
        m.append(t)
    return m

# Get the transformation matrix
transform = get_transfrom_matrix(clists, 31)
A = Matrix(transform)
```

Here's our `matrix A`:

```console
Matrix A
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  1  2  3  4  5]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  1  2  3  4  4]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  1  2  3  3  3]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  1  2  2  2  2]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  1  1  1  1  1]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  0  0  0  0  0  0]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 25 25 25 25 25 25]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 24 24 24 24 24 24 24]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 23 23 23 23 23 23 23 23]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 22 22 22 22 22 22 22 22 22]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 21 21 21 21 21 21 21 21 21 21]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 20 20 20 20 20 20 20 20 20 20 20]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 19 19 19 19 19 19 19 19 19 19 19 19]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 18 18 18 18 18 18 18 18 18 18 18 18 18]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 17 17 17 17 17 17 17 17 17 17 17 17 17 17]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 16 16 16 16 16 16 16 16 16 16 16 16 16 16 16]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15 15]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14 14]
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13 13]
[ 1  2  3  4  5  6  7  8  9 10 11 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12 12]
[ 1  2  3  4  5  6  7  8  9 10 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11]
[ 1  2  3  4  5  6  7  8  9 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10]
[ 1  2  3  4  5  6  7  8  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9  9]
[ 1  2  3  4  5  6  7  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8  8]
[ 1  2  3  4  5  6  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7  7]
[ 1  2  3  4  5  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6  6]
[ 1  2  3  4  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5  5]
[ 1  2  3  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4  4]
[ 1  2  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3  3]
[ 1  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2  2]
[ 1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1]
```

Now, after checking our matrix on one of the input we previsouly submitted to the oracle, it doesn't work! So we don't have a linear transform like `Y = A*X`. But maybe we're just offset, like `Y = A*X + B`. Let's calculate the offset vector `B`:

```python
#It doesn't work... Maybe there's an offset vector, like so: Y = t(A)*X + B
# Let's calculate if using a sample
x = 'aaaaaaaaaaaaaaaaaaaalaaaaaaaaaa'; y = 'rrzzqahtycrcrscxxdvazhmiybzoyej'
ax = encrypt1(x)
v = [(ord(y[j]) - ord(ax[j]))%26 for j in range(31)]
B = vector(v)
print('Vector B')
print(B)
```

```console
Vector B
(6, 21, 18, 7, 13, 12, 8, 9, 3, 22, 0, 11, 0, 1, 11, 6, 6, 12, 4, 9, 8, 16, 21, 17, 7, 10, 8, 23, 7, 13, 18)
```

And now, when checking the encryption `Y = A*X + B` on a sample example, actually gives us the same encrypted output as the oracle! So that's it.

Finally, we can decrypt the message using `X = I*(Y - B)`, where `I is the Inverse matrix of A`:

```python
def decrypt(block):
    y = vector([(ord(c) - ord('a'))%26 for c in block])
    x = I*(y - B)
    dec = ''.join([chr(i%26 + ord('a')) for i in x])
    #print(block, y, x, dec)
    return dec

print('Flag')
print(decrypt(secret))
```

```console
$ python3 sol.py
Flag
lenclumedesjourneesensoleillees
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{lenclumedesjourneesensoleillees}
