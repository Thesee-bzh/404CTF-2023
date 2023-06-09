# Web3 / La Folie du jeu : descente aux enfers 

## Challenge
Alors que vous étiez assis à une table du café Le Procope, vos pensées furent interrompues par l'apparition de la magnifique Marguerite Gauthier. Son regard était aussi pénétrant que ses courbes gracieuses, et son air empreint d'un charme envoûtant ne laissait aucun doute quant à sa nature exceptionnelle.

Elle s'approcha de vous avec grâce, ses pas silencieux comme une promesse d'aventure. Elle vous confia alors les affres qui tourmentaient son âme : c'était à cause d'elle qu'Armand Duval était pris dans une spirale d'addiction aux jeux d'argent qui le détruisait.

Ce n'était pas n'importe quels jeux d'argent qui retenaient Armand prisonnier de leurs charmes sournois. Non, il s'était épris des loteries établies sur la blockchain Ethereum, ces jeux impitoyables où l'espoir et le désespoir se côtoyaient sans relâche, tels des amants inséparables. Ainsi, les dés étaient jetés, et la danse avec le destin commençait. Vous alliez donc vous plonger dans cet univers énigmatique de la blockchain Ethereum, où les paris étaient éternels et les gains fugaces. Pour Marguerite, vous braveriez les tourments, manipuleriez les nombres et les probabilités avec habileté, cherchant à renverser le cours du destin et à redonner à Armand Duval une chance de s'échapper des griffes implacables du jeu.

Les tasses de café fumaient encore devant vous, tandis que vous vous prépariez à affronter les défis à venir. Marguerite vous observait avec un mélange d'inquiétude et d'espoir dans ses yeux. Vous aviez maintenant un objectif commun : sauver l'âme tourmentée d'Armand et lui offrir une nouvelle vie.

Gagnez à la roulette décrite dans le contrat ci-joint :

 
## Inputs
- server at challenges.404ctf.fr:31565
- solidity contract: [Jeu.sol](./Jeu.sol)


## Solution
Here's the contrat: 

```python
// SPDX-License-Identifier: MIT
pragma solidity 0.8.18;

contract Jeu {
    bool public isSolved = false;
    uint public m = 0x7fffffff;
    uint public a = 12345;
    uint public c = 1103515245;

    uint private currentState;

    constructor(uint _start) {
        currentState = _start;
    }

    function guess(uint _next) public returns (bool) {
        currentState = (a * currentState + c) % m;
        isSolved = (_next == currentState) || isSolved;
        return isSolved;
    }
}
```

We need to have variable `isSolved` set to `True`, which we can only do by guessing the next state when calling function `guess()`. To do that, we need the `currentState`, which is a `private variable`... but not that private, since we can access it via its storage slot using method `get_storage_at()`.

Here, `isSolved` is at slot 0, etc. and `currentState` at slot 4.

All we need to do is to get `currentState` at slot 4, predict next state, call `guess()` and verify `isSolved` has been toggled:

```python
is_solved = c.functions.isSolved().call()
print('is_solved', is_solved)

# Get current state at storage position 4
state = int(w3.eth.get_storage_at(addr, 4).hex()[-8:], 16)
print('current_state', hex(state))

# Guess next state
next_ = (12345 * state + 1103515245) % 0x7fffffff
p = c.functions.guess(next_).transact()
print('guess next state', hex(next_))

# Verify we actually solved it
is_solved = c.functions.isSolved().call()
print('is_solved', is_solved)
```

```console
$ python3 sol.py
is_solved False
current_state 0x14691a26
guess next state 0x2144894
is_solved True
```

It should be solved; Let's check it:

```console
$ nc challenges.404ctf.fr 31565
Bienvenue dans l'univers des smart contracts !
JSON-RPC : https://blockchain.challenges.404ctf.fr/
chain ID : 31337
Que voulez-vous faire ?
(...)

Déploiement de Jeu.sol...
Challenge déployé à l'adresse 0xa49385A5db5ADe76fD99827eBaAAc806BbeEaab3

1. Déployer un challenge
2. Utiliser le faucet
3. Vérifier si le challenge est résolu
4. Réinitialiser
5. Quitter

> 3
404CTF{r4Nd0Mn3ss_1S_NOt_s0_345y}

```


## Python code
Complete solution in [sol.py](./sol.py)

## Flag
404CTF{r4Nd0Mn3ss_1S_NOt_s0_345y}
