# Forensics / Le mystère du roman d'amour

## Challenge
En train de faire les cent pas dans un couloir du café se trouve Joseph Rouletabille. Il est préoccupé par un mystère des plus intrigants : une de ses amies, qui écrit régulièrement des livres passionnants, a perdu le contenu de son dernier roman !! Elle a voulu ouvrir son oeuvre et son éditeur a crashé... Il semblerait qu'un petit malin a voulu lui faire une blague et a modifié ses fichiers. Elle n'a pu retrouver qu'un seul fichier étrange, que Joseph vous demande de l'aider à l'analyser afin de retrouver son précieux contenu et de comprendre ce qu'il s'est passé.

Vous devez retrouver le nom de l'amie de Rouletabille, le contenu textuel du brouillon de son livre, ainsi que le chemin vers le fichier en question, le nom de la machine, et le PID du processus crashé.

> Format : 404CTF{PidDuProcessusCrashé-/chemin/vers/le/fichier-nomUser-nomDeLaMachine-contenuDuFichier}

## Inputs
- VIM swap file [fichier-etrange.swp](./fichier-etrange.swp)


## Solution
Running `file` on the swap file gives us the `pid`, `user`, `hostname`, `path/to/file`:
```console
$ file fichier-etrange.swp
fichier-etrange.swp: Vim swap file, version 7.4, pid 168, user jaqueline, host aime_ecrire, file ~jaqueline/Documents/Livres/404 Histoires d'Amour pour les bibliophiles au coeur d'artichaut/brouillon.txt
```

We can recover the swap file and same it to another file:
```console
$ vim -r fichier-etrange.swp
(...)
Using swap file "fichier-etrange.swp"
Original file "~jaqueline/Documents/Livres/404 Histoires d'Amour pour les bibliophiles au coeur d'artichaut/brouill
"~jaqueline/Documents/Livres/404 Histoires d'Amour pour les bibliophiles au coeur d'artichaut/brouillon.txt" [New D
IRECTORY]
Recovery completed. You should check if everything is OK.
(You might want to write out this file under another name
and run diff with the original file to check for changes)
You may want to delete the .swp file now.
```

The recovered file is a PNG file:
```console
$ file recovered.png
recovered.png: PNG image data, 1932 x 1932, 8-bit/color RGBA, non-interlaced
```

![recovered.png](./recovered.png)

Then we look for hidden data in that image. I ended up using `stegsolve` at https://github.com/eugenekolo/sec-tools/tree/master/stego/stegsolve/stegsolve, which reveals a QR code in the gray bits:

![solved.bmp](./solved.bmp)

Reading this QR code using `qrscan` at https://github.com/sayanarijit/qrscan reveals the following message:
```console
$ qrscan solved.bmp
Il était une fois, dans un village rempli d'amour, deux amoureux qui s'aimaient...

Bien joué ! Notre écrivaine va pouvoir reprendre son chef-d'oeuvre grâce à vous !
Voici ce que vous devez rentrer dans la partie "contenu du fichier" du flag : 3n_V01L4_Un_Dr0l3_D3_R0m4N
```

Now we have all the required information to build the flag as requested.

## Flag
404CTF{168-~jaqueline/Documents/Livres/404 Histoires d'Amour pour les bibliophiles au coeur d'artichaut/brouillon.txt-jaqueline-aime_ecrire-3n_V01L4_Un_Dr0l3_D3_R0m4N}
