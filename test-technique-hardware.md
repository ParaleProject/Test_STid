Test technique pour le poste d’ingénieur test et validation hardware.

Objectif
========

L’objectif est de tester le pilotage d’un petit robot.

En partant de la spécification ci-dessous, deux choses vous sont demandées :

1. Proposez quelques idées détaillées de tests à effectuer.
2. Proposez une solution d’automatisation pour un de ces tests.
   Vous pouvez utiliser l’outil ou le langage de programmation que vous
   souhaitez. Idéalement le test doit être fonctionnel, mais nous acceptons
   aussi une solution incomplète.


Spécification
=============

Cette spécification décrit le protocole de communication d’un petit robot très
simple qui ne peut se déplacer que vers l’avant ou l’arrière.

Le robot peut être connecté à un PC, et peut recevoir et envoyer du texte.
Le pilotage s’effectue en envoyant des commandes au format ASCII,
et le robot répond à chaque commande par une ou plusieurs réponses ASCII
également.


Exemple de communication
------------------------

Commande envoyée :

    /01 move 1000
     ┬─ ┬─── ┬───
     │  │    ╰────────── Un argument accepté par la commande
     │  ╰─────────────── Le nom de la commande
     ╰────────────────── L’adresse du robot (car il peut y en avoir plusieurs de connectés)

Réponse reçue :

    @01 OK 0
     ┬─ ┬─ ┬
     │  │  ╰───────── La valeur retournée (0 s’il n’y a pas de donnée particulière)
     │  ╰──────────── OK si la commande a fonctionné, ou RJ si elle a été rejetée
     ╰─────────────── L’adresse du robot qui répond

Exemple avec une autre commande :

    /01 get pos
    @01 OK 550


Liste des commandes
-------------------

- `move` : permet de faire bouger le robot.
  Accepte un argument qui est un nombre représentant la distance à parcourir.
- `get` : permet de lire une donnée du robot.
  Accepte un argument qui est le nom de la donnée. Il y a deux données
  disponibles :
    - `pos` : la position courante du robot (un nombre entier positif ou négatif)
    - `speed` : la vitesse de déplacement du robot (un nombre entier entre 1 et 10).
- `set` : permet de modifier une donnée du robot.
  Accepte deux arguments : le nom de la donnée et la nouvelle valeur. Il n’y a
  qu’une seule donnée modifiable :
    - `speed` : la vitesse de déplacement du robot (un nombre entier entre 1 et 10).
