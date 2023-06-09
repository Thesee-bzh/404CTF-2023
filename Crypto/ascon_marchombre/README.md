# Crypto / ASCON Marchombre

## Challenge
Cela fait maintenant quelques semaines que vous voyagez avec Salim, mais ce que vous attendez le plus chaque jour ce ne sont plus les palpitantes aventures mais plutôt la poésie marchombre que partage avec vous Salim. Vous avez en effet pris goût à écouter les courts poèmes propres à cette guilde qui vous rappellent les haïkus de votre monde.

Ce soir cependant Salim vous met au défi de déchiffrer le code marchombre qui permet de dissimuler les messages qu'il échange avec Ellana et il vous semble alors reconnaitre un chiffrement pas tout-à-fait inconnu ...


## Inputs
> - clef : 00456c6c616e61206427416c2d466172
> - nonce : 0
> - message chiffré : ac6679386ffcc3f82d6fec9556202a1be26b8af8eecab98783d08235bfca263793b61997244e785f5cf96e419a23f9b29137d820aab766ce986092180f1f5a690dc7767ef1df76e13315a5c8b04fb782
> - Données associées : 80400c0600000000

## Solution
Googling around, we discover that `ASCON` is a family of lightweight authenticated ciphers. Looking for some existing decoding in GitHub, we find this implementation: https://github.com/meichlseder/pyascon.

It is implementing this `decrypt` method:

```python
def ascon_decrypt(key, nonce, associateddata, ciphertext, variant="Ascon-128"):
    """
    Ascon decryption.
    key: a bytes object of size 16 (for Ascon-128, Ascon-128a; 128-bit security) or 20 (for Ascon-80pq; 128-bit security)
    nonce: a bytes object of size 16 (must not repeat for the same key!)
    associateddata: a bytes object of arbitrary length
    ciphertext: a bytes object of arbitrary length (also contains tag)
    variant: "Ascon-128", "Ascon-128a", or "Ascon-80pq" (specifies key size, rate and number of rounds)
    returns a bytes object containing the plaintext or None if verification fails
    """
(...)
```

This is exacly what we want. The key is 16 bytes long, so we can assume `Ascon-128` or `Ascon-128a`. Let's try `Ascon-128` as follow:


```python
    key = unhexlify('00456c6c616e61206427416c2d466172')
    nonce = 16 * b'\x00'
    associateddata = unhexlify('80400c0600000000')
    ciphertext = unhexlify('ac6679386ffcc3f82d6fec9556202a1be26b8af8eecab98783d08235bfca263793b61997244e785f5cf96e419a23f9b29137d820aab766ce986092180f1f5a690dc7767ef1df76e13315a5c8b04fb782')
    variant = "Ascon-128"
    pt = ascon_decrypt(key, nonce, associateddata, ciphertext, variant)
    print(pt)
```

```console
$ python3 ascon.py
b"La voie de l'ombre\nEt du silence\n404CTF{V3r5_l4_lum1\xe8r3.}\nEllana"
```
This implementation fails to decode the character `è`, but we can easily fix it and submit the expected flag.

## Flag
404CTF{V3r5_l4_lum1èr3.}
