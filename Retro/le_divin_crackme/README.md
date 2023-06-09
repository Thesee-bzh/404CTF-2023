# Retro / Le divin CrackMe

## Challenge
Jean-Jacques Rousseau vous prend à part : « J'ai déjà raconté la fois où j'ai rencontré le Marquis de Sade ? Non ? Tu en as de la chance... Mes amis avaient plannifié une entrevue entre lui et moi en ville. Avant même de lui parler, il me paraissait étrange. Quoique l'air bien à l'aise, les premiers mots qu'il prononça furent 'Me feriez vous le plaisir de jouer en ma compagnie ?'. Malgré sa demande, j'avais comme l'impression de ne pas vraiment avoir le choix et, en effet, avant de pouvoir lui répondre il poursuivit 'Voici ce que nous allons entreprendre : Vous trouvez mon mot de passe et vous voilà libre. Autrement, je ne réponds plus de rien.'.

Tandis que je m'essayais à son drôle jeu, il me présentait ses points de vue sur les institutions, et, bien que je partage ses opinions sur la nécessité d'accepter l'humain le plus naturel, laissant la corruption des mœurs installée par les institutions derrière nous, je restais critique face à ses aspects les plus libertins... »

« Il serait malvenu de te raconter ce qui se passa par la suite considérant mon échec, mais je suis curieux, aurait tu réussi, toi ? Essaye donc, tu ne risques rien en ce qu'il te concerne ! Pour vérifier que tu ne m'as pas répondu au hasard, j'aimerais que tu me précises avec quel programme le binaire a été compilé ainsi que la fonction spécifique qui est utilisée pour tester le mot de passe. »

> Format : 404CTF{compilateur:fonction:mot_de_passe} | tout en minuscules sauf le mot de passe

## Inputs
- binary: [divin-crackme](./divin-crackme)


## Solution
`Ghidra` decompiles the `main` function as follow:


```c
undefined8 main(void)

{
  int iVar1;
  size_t sVar2;
  char local_48 [10];
  char acStack62 [10];
  char acStack52 [44];

  printf("Mot de passe ? : ");
  __isoc99_scanf("%60s",local_48);
  sVar2 = strlen(local_48);
  if ((((sVar2 == 0x1e) && (iVar1 = strncmp(acStack62,"Ph13_d4N5_",10), iVar1 == 0)) &&
      (iVar1 = strncmp(local_48,"L4_pH1l0so",10), iVar1 == 0)) &&
     (iVar1 = strncmp(acStack52,"l3_Cr4cKm3",10), iVar1 == 0)) {
    printf("Bien joué...");
    return 0;
  }
  printf("Navré...");
  return 1;
}
```
There's a buffer overflow when reading more than 10 characters from the input: following local variables are overflowed. To pass the verification:
- password length must be 0x1e (30)
- local_48 shall contain `L4_pH1l0so`
- 1st overflowed variable `acStack62` shall contain `Ph13_d4N5_`
- 2nd overflowed variable `acStack52` shall contain `l3_Cr4cKm3`

This gives us the password:

```console
$ ./divin-crackme
Mot de passe ? : L4_pH1l0soPh13_d4N5_l3_Cr4cKm3
Bien joué ! Tu aurais été libre, pour cette fois...                                                                  
```

## Flag
404CTF{gcc:strncmp:L4_pH1l0soPh13_d4N5_l3_Cr4cKm3}
