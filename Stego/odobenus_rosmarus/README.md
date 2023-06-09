# Stego / Odobenus Rosmarus

## Challenge
« Bonjour à toi, et bienvenue au café littéraire ! »

 Connais-tu la première règle de la lecture ? Ne pas s'attacher aux mots. Il faut les surpasser, chercher l'idée derrière. L'existence précède l'essence, ici nous cherchons l'essence des choses, et non pas leur existence ou leur forme.

Je te laisse un petit quelque chose. Prouve moi que tu peux lire entre les lignes.


    Format : 404CTF{cequevousalleztrouver}

## Inputs
> Ce soir je Célèbre Le Concert Electro Comme Louis Et Lou. Comme La nuit Commence Et Continue Clairement, Et Clignote Lascivement il Chasse sans Chausser En Clapant Encore Classiquement Les Cerclages du Clergé. Encore Car Encore, Louis Lou Entamant Longuement La Lullabile En Commençant Le Cercle Exhaltant de Club Comique Cannais Et Clermontois.

## Solution
Whats strikes immediately are the uppercase letters at random positions. Also, `Odobenus Rosmarus` is a hint for `Morse`.

So let's assume:
- word starting with `uppercase letter` => `.` (short)
- word starting with `lowercase letter` => `-` (long)

(or the opposite)


```python
s = "Ce soir je Célèbre Le Concert Electro Comme Louis Et Lou. Comme La nuit Commence Et Continue Clairement, Et Clignote Lascivement il Chasse sans Chausser En Clapant Encore Classiquement Les Cerclages du Clergé. Encore Car Encore, Louis Lou Entamant Longuement La Lullabile En Commençant Le Cercle Exhaltant de Club Comique Cannais Et Clermontois."

# Extract uppercase letters (and dots)
out = ""
for c in s:
    if c.isupper() or c == '.':
        out += c
print(out)

# CCLCECLEL.CLCECCECLCCECECLCC.ECELLELLLECLCECCCEC.
# This is Morse: C for 'Court' (short), L for Long
morse = out
morse = morse.replace('.', '/')
morse = morse.replace('C', '.')
morse = morse.replace('L', '-')
morse = morse.replace('E', ' ')
print(morse)
```

```console
$ python3 sol.py                 
CCLCECLEL.CLCECCECLCCECECLCC.ECELLELLLECLCECCCEC.
..-. .- -/.-. .. .-.. . .-../ . -- --- .-. ... ./
```

Finally, we deocde it with `dcode`: `FACILELEMORSE`

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{FACILELEMORSE}
