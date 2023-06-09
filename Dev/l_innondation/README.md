# Dev / L'innondation

## Challenge
Vous prenez une collation accolé au bar du Procope, et remarquez au bout d'une dizaine de minutes un post-it, sur lequel votre nom est écrit, et en dessous une inscription : « Salut, le nouveau, viens à ma rencontre, porte de derrière ».
Curieux, vous sortez du café par cette porte et tombez nez à nez avec un jeune homme.

« Bonjour, pouquoi ce post-it ?

— Salut ! Excellente question. Dernièrement, un évènement étrange a bouleversé ma ville : elle a été prise d'une épidémie de gens se transformant en rhinocéros. Alors que ce n'était jusqu'hier qu'une dizaine de gens qui étaient touchés, j'ai vu ce matin un troupeau de ce qui semblait être plusieurs centaines de rhinocéros passer sous ma fenêtre. J'ai aussitôt saisi mon appareil photo et photographié régulièrement le troupeau pour avoir une estimation du nombre de rhinocéros, mais il y en a bien trop pour compter tout ça à moi seul ou même à deux.

— Certes, et où voulez-vous donc en venir ?

— Voyez-vous, j'ai entendu parler de vos talent dans les nouvelles technologies par le biais d'un ami qui fréquente ce café. J'imagine qu'un ordinateur saura compter bien plus vite que nous deux, ça vous dirait de m'aider ? D'ailleurs, on ne s'est toujours pas présentés. Moi, c'est Béranger. »

## Inputs
- server at challenges.404ctf.fr:31420

## Solution
When connecting to the server, we're asked to count some rhinos  graphically displayed with ascii string ``~c`°^)`` like so:

```console
$ nc challenges.404ctf.fr 31420
« Allez, vite, il y a une pile de photos assez importante à traiter,
comptes-moi le nombre de rhinos par photo. »
 ~c`°^)                               ~c`°^)        ~c`°^)                 ~c`°^)       ~c`°^)
                          ~c`°^)                    ~c`°^)                  ~c`°^)        ~c`°^)
  ~c`°^)                    ~c`°^)                 ~c`°^)       ~c`°^)
  ~c`°^)                                                                              ~c`°^)
                           ~c`°^)       ~c`°^)                            ~c`°^)
               ~c`°^)       ~c`°^)                            ~c`°^)
                ~c`°^)        ~c`°^)   ~c`°^)     ~c`°^)      ~c`°^)                     ~c`°^)
    ~c`°^)                 ~c`°^)     ~c`°^)                                 ~c`°^)
      ~c`°^)   ~c`°^)                            ~c`°^)
   ~c`°^)                            ~c`°^)
  ~c`°^)      ~c`°^)     ~c`°^)          ~c`°^)     ~c`°^)                             ~c`°^)
  ~c`°^)     ~c`°^)          ~c`°^)                             ~c`°^)     ~c`°^)   ~c`°^)
                            ~c`°^)   ~c`°^)                             ~c`°^)
     ~c`°^)     ~c`°^)                  ~c`°^)                                ~c`°^)
    ~c`°^)                                                                   ~c`°^)    ~c`°^)
 ~c`°^)                    ~c`°^)   ~c`°^)                       ~c`°^)
    ~c`°^)              ~c`°^)                       ~c`°^)
                              ~c`°^)                            ~c`°^)                   ~c`°^)
~c`°^)
      ~c`°^)     ~c`°^)    ~c`°^)               ~c`°^)           ~c`°^)       ~c`°^)
                                    ~c`°^)                        ~c`°^)     ~c`°^)       ~c`°^)
                ~c`°^)                                ~c`°^)                             ~c`°^)
                             ~c`°^)                                                   ~c`°^)
~c`°^)           ~c`°^)       ~c`°^)     ~c`°^)       ~c`°^)     ~c`°^)   ~c`°^)        ~c`°^)
     ~c`°^)                               ~c`°^)     ~c`°^)                 ~c`°^)
                              ~c`°^)                                      ~c`°^)
                  ~c`°^)              ~c`°^)                                ~c`°^)       ~c`°^)
                 ~c`°^)                           ~c`°^)
     ~c`°^)                 ~c`°^)    ~c`°^)        ~c`°^)                            ~c`°^)
  ~c`°^)        ~c`°^)    ~c`°^)        ~c`°^)       ~c`°^) ~c`°^)        ~c`°^)
              ~c`°^)                     ~c`°^)
  ~c`°^)        ~c`°^)       ~c`°^) ~c`°^)        ~c`°^)       ~c`°^)    ~c`°^)
Combien de rhinocéros comptez-vous dans cette image ?
Votre réponse :
>
```

Counting the number of rhinos is easy: we receive the all blob until the next prompt `>`. Then we need to do it in a loop, because of course the server doesn't ask it just once ! After a hundred iterations or so, the're finally granted with the flag. Here's the python code, where `pwntools` is used to interact with the server:


```python
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
```

And here's the end of the execution:
```console
                                          ~c`°^)                  ~c`°^)
                              ~c`°^)    ~c`°^)        ~c`°^)                           ~c`°^)
  ~c`°^)          ~c`°^)    ~c`°^)        ~c`°^) ~c`°^)
Combien de rhinocéros comptez-vous dans cette image ?
Votre réponse :
>
125

« Très bien, la suite arrive ! »

« Bien joué ! Avant que tu partes, ta récompense. »



Il vous tend une enveloppe.

 « Ouvres-la une fois qu'il n'y a personne autour de toi. »

Vous faites exactement cela, à l'intérieur se trouve un billet, et une lettre. Dessus il est marqué 404CTF{4h,_l3s_P0uvo1rs_d3_l'iNforM4tiqu3!}

[*] Closed connection to challenges.404ctf.fr port 31420

```

## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{4h,_l3s_P0uvo1rs_d3_l'iNforM4tiqu3!}
