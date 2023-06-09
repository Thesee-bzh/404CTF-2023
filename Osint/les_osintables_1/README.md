# OSINT / Les OSINTables (1/3)

## Challenge
n pleine discussion au Procope, Cosette vous raconte autour d'une part de fraisier la première fois qu'elle a essayé d'envoyer une lettre à son bienfaiteur : Jean Valjean.
 
Débutante dans la démarche postale, elle s'est trompée sur les informations nécessaires, elle en a même oublié l'adresse du destinataire, n'écrivant que la sienne. Elle vous montre la photo ci-jointe et vous met au défi de trouver d'où elle l'a écrite.

Trouvez l'adresse d'envoi de la lettre (celle de Cosette).

> Format : 404CTF{numero_adresse_rue_ville}

exemple : 404CTF{36_quai_des_orfevres_paris}

## Inputs
![photo.jpg](./photo.jpg)

## Solution
LXXXIII (83) rue Victor Hugo, Ve.....
- Versailles: doesn't work
- Vergèze: works !

## Flag
404CTF{83_rue_victor_hugo_vergeze}
