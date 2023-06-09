# Dev / Des mots, des mots, des mots

## Challenge
Prenant du bon temps à votre table en lisant un livre, vous buvez une gorgée de café. En baissant votre tasse, vous remarquez à travers la fenêtre une petite silhouette, elle semble chercher quelque chose ou quelqu'un.

Cette intrigante situation vous pousse à aller à sa rencontre. La silhouette est en réalité une jeune fille rousse. Vos regards se croisent, elle a l'air perdue. Vous la rejoignez, et lui demandez :

« Bonjour, puis-je t'aider ?

— Oui. Je cherche à traduire un texte selon des règles étranges mot à mot. Il s'agit d'un livre nommé Les Misérables. Peux-tu m'aider ? Au fait, moi c'est Cosette !

— Je vois, aucun problème. Je peux justement te faire un script qui va transformer chaque mot de ton texte. Quelles sont ces règles ?

— Je vais tout t'expliquer, allons nous installer à l'intérieur.»

Elle vous suit à votre table et vous vous mettez au travail.

Indications :

    - Les voyelles sont {a, e, i, o, u, y}.
    - L'indiçage commence à 0.
    - Les règles sont données en Markdown. Les _ dans les exemples sont des balises italique Markdown et ne comptent pas dans l'exemple.
    - Les règles sont à appliquer les une après les autres. Typiquement pour la règle 2 il faut partir du résultat de la règle 1, et ainsi de suite.
    - Le symbole ^ correspond à l'opérateur puissance.


## Inputs
- server at challenges.404ctf.fr:30980


## Solution
First we are presenting some rules to apply on words (like inverting the order of the letters, etc.), the rules get more complex one after the other. At the end, we're given a all text (a list of words) and we need to apply all rules, in order, on each single word. So we need to automate the all process (using `pwntools` to interact with the server) and to implement the different rules.

### Rule 0

```console
Commençons. Je te propose de démarrer en transformant mon nom.
Tout d'abord retourne mon nom sans modifications.
Règle 0 : Aucune modification
Entrée :
{cosette}
cosette
>> Je vois que tu as compris. La première règle de ce langage est très simple.
```

### Rule 1
```console
Règle 1 : Inverser les lettres
Entrée :
{cosette}
ettesoc
>> Oui c'est bien. Maintenant la deuxième règle est un peu plus difficile.
```

Python code to implement that rule:
```python
def r1_op(req):
    resp = req[::-1]
    return resp
```

### Rule 2
```console
Règle 2 :
- Si le mot à un nombre de lettres pair, échanger la 1ere et la 2e partie du mot obtenu
- Sinon, enlever toutes les lettres du mot correspondant à la lettre centrale
Entrée :
{cosette}
ttsoc
>> Tu t'en sors très bien ! Continuons avec la troisième règle.
```

Python code to implement that rule:
```python
def r2_op(req):
    l = len(req)
    if l % 2 == 0:
        # - Si le mot à un nombre de lettres pair, échanger la 1ere et la 2e partie du mot obtenu
        resp = req[l//2:] + req[:l//2]
        return resp
    else:
        # - Sinon, enlever toutes les lettres du mot correspondant à la lettre centrale
        c = req[l//2]
        resp = req.replace(c, '')
        return resp
```

### Rule 3
Here there was a trap: the modification shall be applied on the `original word`, not the word resulting from the application of previous rules. That one got me for a long time...

```console
Règle 3 :
_Si le mot a 3 lettres ou plus_ :

- Si la 3e lettre du mot obtenu est une consonne, "décaler" les voyelles vers la gauche dans le mot original, puis réappliquer les règles 1 et 2.
- Sinon : la même chose mais les décaler vers la droite.

> Ex de décalage : _poteau => petauo_ // _drapeau => drupaea_
Entrée :
{cosette}
ottsc
>> Nous avons presque fini, la quatrième règle est la plus complexe.
```

Python code to implement that rule:
```python
def r3_op(req, orig):
    # Si le mot a 3 lettres ou plus :
    # - Si la 3e lettre du mot obtenu est une consonne:
    #   => "décaler" les voyelles vers la gauche dans le mot original, puis réappliquer les règles 1 et 2.
    # Sinon : la même chose mais les décaler vers la droite.
    # Ex de décalage : _poteau => petauo_ // _drapeau => drupaea_
    if len(req) < 3:
        return req
    # Extract voyels and positions from original word:
    v = deque([c for c in orig if c in 'aeiouy'])
    p = [i for i in range(len(orig)) if orig[i] in 'aeiouy']
    if req[2] in 'aeiouy':
        # Shift voyels to the right
        v.rotate(1); op = '->'
    else:
        # Shift voyels to the left
        v.rotate(-1); op = '<-'
    resp = orig
    # Replace voyels with shifted ones in original word
    l = list(resp)
    for i in range(len(p)):
        l[p[i]] = list(v)[i]
    resp = ''.join(l)
    resp = r1_op(resp)
    resp = r2_op(resp)
    return resp
```

### Rule 4
That one was a bit of a nightmare; Tons of debug needed...

```console
Règle 4 :
- Pour `n` allant de 0 à la fin du mot, si le caractère `c` à la position `n` du mot est une consonne (majuscule ou minuscule), insérer en position `n+1` le caractère de code ASCII `a = ((vp + s) % 95) + 32`, où `vp` est le code ASCII de la voyelle précédant la consonne `c` dans l'alphabet (si `c = 'F'`, `vp = 'E'`), et `s = SOMME{i=n-1 -> 0}(a{i}*2^(n-i)*Id(l{i} est une voyelle))`, où `a{i}` est le code ASCII de la `i`-ième lettre du mot, `Id(x)` vaut `1` si `x` est vrai, `0` sinon, et `l{i}` la `i`-ième lettre du mot. _Attention à bien appliquer cette règle aussi sur les caractères insérés au mot._

> Ex : _futur => f&ut\ur@_

- Enfin, trier le mot par ordre décroissant d'occurrences des caractères, puis par ordre croissant en code ASCII pour les égalités

> Ex de tri : _patate => aattep_
Entrée :
{cosette}
PPtt!15QRUWcos
>> Bravo ! Maintenant je vais te donner un chapitre dont j'ai besoin de la traduction complète.
```

Python code to implement that rule:
```python
def r4_op(req):
    # Pour `n` allant de 0 à la fin du mot,
    # - si le caractère `c` à la position `n` du mot est une consonne (majuscule ou minuscule):
    #   => insérer en position `n+1` le caractère de code ASCII `a = ((vp + s) % 95) + 32`, où
    #      * `vp` est le code ASCII de la voyelle précédant la consonne `c` dans l'alphabet
    #        (si `c = 'F'`, `vp = 'E'`), et
    #      * `s = SOMME{i=n-1 -> 0}(a{i}*2^(n-i)*Id(l{i} est une voyelle))`, où
    #        ** `a{i}` est le code ASCII de la `i`-ième lettre du mot,
    #        ** `Id(x)` vaut `1` si `x` est vrai, `0` sinon, et
    #        ** `l{i}` la `i`-ième lettre du mot.
    # Attention à bien appliquer cette règle aussi sur les caractères insérés au mot.
    # > Ex : _futur => f&ut\ur@_
    # - Enfin, trier le mot par ordre décroissant d'occurrences des caractères,
    #   puis par ordre croissant en code ASCII pour les égalités
    # > Ex de tri : _patate => aattep_
    w = list(req)
    alphabet_lowercase = list(string.ascii_lowercase)
    alphabet_uppercase = list(string.ascii_uppercase)
    #print('r4', word, r3, ''.join(w))
    n = 0
    while n < len(w):
        c = w[n]
        if c in 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ':
            # c can be uppercase or lowercase
            if c.isupper():
                alphabet = alphabet_uppercase; voyels = 'AEIOUY'
            else:
                alphabet = alphabet_lowercase; voyels = 'aeiouy'

            # vp: voyel preceding c in the alphabet (can be uppoercase of lowercase)
            pos = alphabet.index(c)
            alphabet = alphabet[:pos+1]
            prev_v = list(deque([x for x in alphabet if x in voyels]))[-1:][0]
            vp = ord(prev_v)
            #print('\t', 'n:', n, 'c:', c, 'prev:', prev_v)

            # s = SOMME{i=n-1 -> 0}(a{i}*2^(n-i)*Id(l{i} est une voyelle))
            s = 0
            for i in range(n-1, -1, -1):
                if w[i] in 'aeiouyAEIOUY':
                    ai = ord(w[i])
                    s += ai*pow(2, n-i)
            s = int(s)

            # Insert a = ((vp + s) % 95) + 32 at position n+1
            a  = ((vp + s) % 95) + 32
            w.insert(n+1, chr(a))
            #print('\t\t==>', 'vp', vp, 's', s, 'a', a, 'chr(a):', chr(a), ''.join(w))

        # Increase n
        n += 1

    # Sort by occurence in decreasing order (egality: by ascii code in increasing order)
    # First sort by ascii code in increasing order and count occurences
    chars = sorted(list(set(w)))
    occs  = [w.count(c) for c in chars]
    # Then sort by occurence in decreasing order
    s = ''
    for occ in range(len(w), 0, -1):
        for i in range(len(chars)):
            if occs[i] == occ:
                s += chars[i] * occ

    # Finally return the joined string
    #print('\t', ''.join(w), 'chars:', ''.join(chars), 'occs:', occs, ''.join(s), [ord(c) for c in s])
    return ''.join(s)
```

### Text
```
Chaque mot est écrit en minuscule sans accents ni caractères spéciaux et sont séparés par un espace. Tu as 5 secondes pour répondre.
Entrée :
{avait premier quart siecle montfermeil paris facon gargote existe aujourd cette gargote etait tenue appeles thenardier femme etait situee ruelle boulanger voyait dessus porte planche clouee cette planche etait peint quelque chose ressemblait homme portant autre homme lequel avait grosses epaulettes general dorees larges etoiles argentees taches rouges figuraient reste tableau etait fumee representait probablement bataille lisait cette inscription sergent waterloo ordinaire tombereau charrette porte auberge cependant vehicule mieux fragment vehicule encombrait devant gargote sergent waterloo printemps certainement attire masse attention peintre passe etait avant train fardiers usites forets servent charrier madriers troncs arbres avant train composait massif essieu pivot}
aa0:tv PPeerr01Eip 004aqrt BBeess#,AGQSTXbcfghikln mmoo)*9:ABRTcfilnrt~ 09BLRTaiprs *NZ[afno PP1aeort~ ee5BQRUirstxy JJ"+0adjor ee;FNc PP1aeort~ tt0<ae ee2Ftu ppp.05@QRals eeeddhhrr+,36GOTXaint eeAJRf tt0<ae ee0\istu eell',GTXhru} FF'*0?Oabglnoru 7Iahiortvy sssssdd03ENW_befu PP'1eopt pp&*25Waceghl eeIVclnou{ ee;FNc pp&*25Waceghl tt0<ae **0Dinpt eeqquu&5 EEPPcc1KThos ssseerr03>CDMSVW\_`abdfilqtv ehior PP*1anopr~ \aeru ehior eell0QV^nqu{ aa0:tv 9egor| eee**PPtt18D_alpsu <<ee*:BZglnrz ee.0`dors .06`aeglrs **0Dilost eee,,GGTTXXhh#0Zagrst ".<`acehst Y[egiorstu iiirr*0?aefgjntu~ ee<=rt aabbssNW_deitu tt0<ae ee[fu eeerrrpptt/05<@KLQRU`ains aabbee"*.5CDSV\lmnopqrtuz{ __aabbllss/4KLNWdeit ii.0@alst ee;FNc PPnn!*15QRUW\coprst{ ee*0<=nrst oo-4;<WXaelrtvw **iirrDHIRadeo !'>FNabmortu~ eett-4>@ach PP'1eopt bb'*@CDagru ee.05Vacdpt~ CCeehh+2<ciluv{ 6AQSbefgkmnsux 88JJ&+<@KVaefgmnrstvx CCeehh+2<ciluv{ BB#&*:ACSV\abceikmnoqrt &/6@KLadejntv PP1aeort~ ee*0<=nrst oo-4;<WXaelrtvw 00pp*4>Geimnrs} eeettt""\\nnuu=CMPSVacimr 00tt\aeir >aem ttt"2FIXaefgio ee+<`diprt *Daep tt0<ae *06ntv *4@anrt 22rr"0`adefis ss #\eitu 220`eforst ee*0<=nrst rrrr!0:CSV\acehiq{ rr"026`adeims PPnn!15QRUVWcorst{ rr"05<abes *06ntv *4@anrt /04@AKLacijmpst ssvv0>Yacfimw| 00eessiu )0gioptx
>> Merci ! C'est exactement ce qu'il me fallait !

Voici ta récompense : 404CTF{:T]cdeikm_)W_doprsu_nt_;adei}
```

Python code to implement that final piece:
```python
def r_op(req):
    words = req.split()
    resp = ' '.join([r4_op(r3_op(r2_op(r1_op(w)), w)) for w in words])
    return resp
```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{:T]cdeikm_)W_doprsu_nt_;adei}
