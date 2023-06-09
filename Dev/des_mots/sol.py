from pwn import *
from collections import deque
import string


target = remote('challenges.404ctf.fr', 30980)

def get_question(q):
    try:
        line = target.recvuntil(q.encode()); print(line.decode())
    except:
        return False

def get_input():
    line = target.recvuntil("Entrée : ".encode()); print(line.decode().strip())
    line = target.recvline(); print(line.decode().strip())
    req = line.strip().decode()[1:-1]
    return req

def send_response(req):
    target.send(req.encode() + b'\n'); print(req)
    q = target.recvline(); print(q.decode())

def r0(q):
    get_question(q)
    send_response(get_input())

def r1_op(req):
    resp = req[::-1]
    #print('r1', req, resp)
    return resp
    
def r1(q):
    get_question(q)
    send_response(r1_op(get_input()))

def r2_op(req):
    l = len(req)
    if l % 2 == 0:
        # - Si le mot à un nombre de lettres pair, échanger la 1ere et la 2e partie du mot obtenu
        resp = req[l//2:] + req[:l//2]
        #print('r2 pair', l, req, resp)
        return resp
    else:
        # - Sinon, enlever toutes les lettres du mot correspondant à la lettre centrale
        c = req[l//2]
        resp = req.replace(c, '')
        #print('r2 impair', l, req, c, resp)
        return resp

def r2(q):
    get_question(q)
    send_response(r2_op(r1_op(get_input())))

def r3_op(req, orig):
    # Si le mot a 3 lettres ou plus :
    # - Si la 3e lettre du mot obtenu est une consonne:
    #   => "décaler" les voyelles vers la gauche dans le mot original, puis réappliquer les règles 1 et 2.
    # Sinon : la même chose mais les décaler vers la droite.
    # Ex de décalage : _poteau => petauo_ // _drapeau => drupaea_
    if len(req) < 3:
        #print('r3', w, r2, len(req), req[2], 'None')
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
    #print('r3', req, req[2], 'orig:', orig, op, resp)
    resp = r1_op(resp)
    resp = r2_op(resp)
    #print('r3', req, req[2], 'orig:', orig, op, resp)
    return resp

def r3(q):
    get_question(q)
    orig = get_input()
    send_response(r3_op(r2_op(r1_op(orig)), orig))

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

def r4(q):
    get_question(q)
    orig = get_input()
    send_response(r4_op(r3_op(r2_op(r1_op(orig)), orig)))

def r_op(req):
    words = req.split()
    resp = ' '.join([r4_op(r3_op(r2_op(r1_op(w)), w)) for w in words])
    return resp

def r_(q):
    get_question(q)
    send_response(r_op(get_input()))

def get_rest():
    while True:
        q = target.recvline(); print(q.decode().strip())
        if b'404CTF' in q:
            break

def main():
    r0("Règle 0 : Aucune modification")
    r1("Règle 1 : Inverser les lettres")
    r2("Règle 2 :")
    r3("Règle 3 :")
    r4("Règle 4 :")
    r_("Chaque mot est écrit en minuscule sans accents ni caractères spéciaux et sont séparés par un espace. Tu as 5 secondes pour répondre.")
    get_rest()

main()

