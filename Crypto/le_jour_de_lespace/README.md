# Crypto / Le Jour de l'espace

## Challenge
Rimbaud vous propose une séance initiatique au Oui-ja dans l'aile mystique du café littéraire (oui, oui, ça existe), vous avez une vision ésotérique :

Alors que vous voyez le texte suivant `ueomaspblbppadgidtfn`, Rimbaud vous décrit voir un étrange cadre de 50cm de côté, avec des petits carrés de 10cm de côtés, numérotés de 0 à 24 et jetés pêle-mêle sur le sol. Rimbaud n'y comprends rien, mais vous restez obsédé par cette idée, et décidez de résoudre l'énigme.

Toutes les informations nécéssaires à la résolution de ce challenge sont présentes dans l'énoncé ci-dessus.

> Format : 404CTF{cequevousalleztrouver}


## Inputs
- server at challenges.404ctf.fr:31451


## Solution
Interacting with the server shows that valid input use characters `a` to `y` (`z` is not valid), the input is encrypted with a `block size = 5`. Also, the blocks are encrypted independantly:
```console
$ nc challenges.404ctf.fr 31451
bienvenue dans loracle. Le message a dechiffrer est : ueomaspblbppadgidtfn
message en clair : a
message chiffre  : aaaaa

message en clair : b
message chiffre  : jlfnt

message en clair : c
message chiffre  : swkbn

message en clair : bbbbb
message chiffre  : jrpaj

message en clair : bbbbbccccc
message chiffre  : jrpajsjfas
```

Bruteforcing is not an option though, that's still too many comninations to test on the remote server. Let's try to find some relation between the input and the output. We're going to use the following input, where only one character is changed at a time, at each position of the block:

```python
# Lets input small variations on blocks of size=5 to see the effect on the output:
wlist1 = ['aaaaa','baaaa','caaaa','daaaa','eaaaa']
wlist2 = ['aaaaa','abaaa','acaaa','adaaa','aeaaa']
wlist3 = ['aaaaa','aabaa','aacaa','aadaa','aaeaa']
wlist4 = ['aaaaa','aaaba','aaaca','aaada','aaaea']
wlist5 = ['aaaaa','aaaab','aaaac','aaaad','aaaae']
```

We use the server as an oracle to encrypt those chosen plaintext blocks. Here the code to interact with the server and retrieve the encrypted blocks for each input:
```python
def oracle(wlist):
    clist = list()
    for w in wlist:
        #message en clair : a
        #message chiffre  : aaaaa
        q = b'message en clair : '
        c.recvuntil(q); #print(q.decode())
        c.send(w.encode() + b'\n')
        line = c.recvline(); #print(line.decode())
        if b'message chiffre' not in line:
            assert()
        ct = line.split()[-1:][0].decode()
        clist.append(ct)
    return clist

wlists = [wlist1, wlist2, wlist3, wlist4, wlist5]
for l in wlists:
    print(l, oracle(l))
```

Here's the output:
```console
$ python3 sol.py
[+] Opening connection to challenges.404ctf.fr on port 31451: Done
bienvenue dans loracle. Le message a dechiffrer est : ueomaspblbppadgidtfn

['aaaaa', 'baaaa', 'caaaa', 'daaaa', 'eaaaa'] ['aaaaa', 'jlfnt', 'swkbn', 'cipoh', 'ltucb']
['aaaaa', 'abaaa', 'acaaa', 'adaaa', 'aeaaa'] ['aaaaa', 'eagov', 'iamdr', 'masrn', 'qaygj']
['aaaaa', 'aabaa', 'aacaa', 'aadaa', 'aaeaa'] ['aaaaa', 'schpw', 'leoft', 'egvuq', 'widkn']
['aaaaa', 'aaaba', 'aaaca', 'aaada', 'aaaea'] ['aaaaa', 'ubkqx', 'pcuhv', 'kdfxt', 'fepor']
['aaaaa', 'aaaab', 'aaaac', 'aaaad', 'aaaae'] ['aaaaa', 'idmry', 'qgyjx', 'yjlbw', 'hmxsv']
```

Now let's find some relation between the input and the output of these choosen plaintext blocks. For instance, in the first line, when the first character is modified by 1 `(a, b, c, d, e), the output's first character is modified by 9 modulo 25 `(a, j, s, c, l). So there's some linearity there. And we can find other linear relation all over the place.

So we make the assumption that there's a `linear transformation`, that can be defined by a `matrix 5x5`, that transforms the input into the output. By the way, the description of the challenge is a clear reference to a matrix 5x5.

To identify this matrix, we need to compute all coefficients `ai,j`, which describe how character `i` in the input affects character `j` in the output (modulo 25). Modulo 25, because letter `z` is not a valid character, which is also suggested by the challenge description.

Let's compute the differences in the outputs to get the coefficients. In the example below, we compute the difference between `(a, j, s, c, l)` for the output's first character, then `(a, l, w, i, t)` for the output's second character, etc. Doing so, we expect to find a constant difference, which we do ! This tells us how the input's first character inpacts the output. Of course, we need to repeat that for other choosen plaintext blocks.
```
['aaaaa', 'baaaa', 'caaaa', 'daaaa', 'eaaaa'] ['aaaaa', 'jlfnt', 'swkbn', 'cipoh', 'ltucb']
```

Here's the python code for it. The output is the transformation matrix:
```python
def get_transform(clist):
    dlist = list()
    # loop on characters in block
    for i in range(0, 5):
        # loop on encrypted blocks
        for j in range(len(clist)-1):
            w1 = clist[j]; w2 = clist[j+1]
            diff = (ord(w2[i]) - ord(w1[i])) % 25
            # Make sure we have a constant difference
            if j != 0 and diff != delta:
                assert()
            delta = diff
        dlist.append(delta)
    return(dlist)

def get_transfrom_matrix(clist):
    m = list()
    for l in clist:
        t = get_transform(l)
        m.append(t)
    return m

# Get the transformation matrix
transform = get_transfrom_matrix(clists)
A = Matrix(transform)
print(A)
```

Here's our transformation matrix:
```
[ 9 11  5 13 19]
[ 4  0  6 14 21]
[18  2  7 15 22]
[20  1 10 16 23]
[ 8  3 12 17 24]
```

Then a bit of maths: we have: `t(A)*x = y` with t(A) the transpose matrix. So `x = (t(A))^-1 * y`. Here you go with sage:
```python
# So we need to transpose and inverse A
T = A.transpose()
I = T.inverse()
```

And here's some code to implement the decryption of a block:

```python
def decrypt(block):
    y = vector([(ord(c) - ord('a'))%25 for c in block])
    x = I*y
    dec = ''.join([chr(i%25 + ord('a')) for i in x])
    #print(block, y, x, dec)
    return dec
```

Finally, we decode each block (I also make sure that when encrypting it again, I get back to the original block):
```python
def flag(chunks):
    dec = list()
    for chunk in chunks:
        x  = decrypt(chunk)
        x_ = encrypt(x)
        if x_ != chunk:
            assert()
        dec.append(x)
    return ''.join([w for w in dec])

print(flag(chunks))
```

This finally gives us the flag:

```console
$ python3 sol.py
[+] Opening connection to challenges.404ctf.fr on port 31451: Done
bienvenue dans loracle. Le message a dechiffrer est : ueomaspblbppadgidtfn

['aaaaa', 'baaaa', 'caaaa', 'daaaa', 'eaaaa'] ['aaaaa', 'jlfnt', 'swkbn', 'cipoh', 'ltucb']
['aaaaa', 'abaaa', 'acaaa', 'adaaa', 'aeaaa'] ['aaaaa', 'eagov', 'iamdr', 'masrn', 'qaygj']
['aaaaa', 'aabaa', 'aacaa', 'aadaa', 'aaeaa'] ['aaaaa', 'schpw', 'leoft', 'egvuq', 'widkn']
['aaaaa', 'aaaba', 'aaaca', 'aaada', 'aaaea'] ['aaaaa', 'ubkqx', 'pcuhv', 'kdfxt', 'fepor']
['aaaaa', 'aaaab', 'aaaac', 'aaaad', 'aaaae'] ['aaaaa', 'idmry', 'qgyjx', 'yjlbw', 'hmxsv']
[ 9 11  5 13 19]
[ 4  0  6 14 21]
[18  2  7 15 22]
[20  1 10 16 23]
[ 8  3 12 17 24]
barjavelmaassassinea
[*] Closed connection to challenges.404ctf.fr port 31451
```

Seems that the trailing `a` is some padding and can be skipped.

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{barjavelmaassassine}
