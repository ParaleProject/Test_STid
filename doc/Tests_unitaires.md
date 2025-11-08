
# Sommaire

[Introduction](#introduction)

[Cas de test N°1: Syntaxe des commandes](#cas-de-test-n1-syntaxe-des-commandes)

[Cas de test N°2: Commande "get"](#cas-de-test-n2-commande-get)

[Cas de test N°3: Commande "set"](#cas-de-test-n3-commande-set)

[Cas de test N°4: Commande "move"](#cas-de-test-n4-commande-move)

[Cas de test N°5: Vérification du déplacement](#cas-de-test-n5-vérification-du-déplacement)

# Introduction

Ce document défini les règles d'exécution et permet d'effectuer les tests unitaires du projet "Robot".

Afin de réaliser les tests correctement, l'environnement ainsi que le robot doit être défini avec les paramètres suivant:

-   La liaison série est configuré sur le port "COM3" du PC
    -   9600 bauds
    -   1s timeout
    -   8 bits de data
    -   1 bit de stop
    -   1 bit de parité (impaire)

-   La position du robot doit être initialisé à 0
-   La vitesse du robot doit être initialisé à 1

La liaison série est considérée comme active et fonctionnelle lors de ces tests.

Les règles à prendre en compte pour ces tests sont:

-   Les valeurs décimales ne sont pas acceptées et renvoie une erreur
-   Une commande incorrecte renvoie toujours "0"
    -   Exemple: /01 set speed 3,5 =\> \@01 RJ 0
    -   Exemple: /01 get =\> \@01 RJ 0
-   1 seul robot sera connecté sur le port "COM3" du PC
-   La vitesse du robot lors des tests est prise en compte dans le temps de déplacement.
-   La vitesse du robot est en unité/seconde
-   La commande "move" ne peux pas dépasser 1000 unités (avant et arrière)
    -   Exemple: /01 move 600 =\> \@01 OK 0
    -   Exemple: /01 move 1300 =\> \@01 RJ 0
-   Le buffer de communication est dit illimité et donc ne sera pas vérifier
    -   Exemple: (/01 move 10) envoyé 40 fois en 1 seconde =\> (@01 OK 0) 40 fois, donc /01 get pos =\> \@01 OK 400

# Cas de test N°1: Syntaxe des commandes

**Description :**

Vérifier le bon fonctionnement des commandes envoyées au robot

**Besoins :**

Robot alimenté et connecté au PC, l'identifiant du robot doit être configuré à 1, la liaison série est configurée et fonctionnelle, un seul robot doit être actif, les valeurs du robot sont réinitialisées (vitesse à 1 et position à 0)

| Étape | Description | Commande | Réponse reçue | Réponse attendue |
|-------|-------------|----------|---------------|------------------|
|1|Envoyer une commande correcte|/01 get pos||@01 OK 0|
|2|Envoyer une commande incorrecte|/01 run 10||@01 RJ 0|
|3|Envoyer une commande avec un identifiant invalide|/00 get pos||Pas de réponse|
|4|Envoyer une commande avec un identifiant inaccessible|/20 get pos||Pas de réponse|
|5|Envoyer une commande sans « / »|01 get pos||Pas de réponse|
|6|Envoyer une commande sans adresse|/ get pos||Pas de réponse|
|7|Vérifier la tolérance de la commande en ajoutant un espace au début|‘ ‘/01 get pos||@01 OK 0|
|8|Vérifier la tolérance de la commande en ajoutant un espace à la fin|/01 get pos’ ‘||@01 OK 0|
|9|Vérifier la tolérance de la commande en ajoutant un espace au milieu|/01 get ’ ‘pos||@01 OK 0|

# Cas de test N°2 : Commande « get »

**Description :**

Vérifier le bon fonctionnement de la commande « get » et de la récupération des valeurs de vitesse et de position du robot

**Besoins :**

Robot alimenté et connecté au PC, l'identifiant du robot doit être configuré à 1, la liaison série est configurée et fonctionnelle, un seul robot doit être actif, les valeurs du robot sont réinitialisées (vitesse à 1 et position à 0)

| Étape | Description | Commande | Réponse reçue | Réponse attendue |
|-------|-------------|----------|---------------|------------------|
|1|Déterminer la valeur de la vitesse à 5|/01 set speed 5||@01 OK 0|
|2|Vérifier si la commande « get speed » récupère la bonne valeur (5)|/01 get speed||@01 OK 5|
|3|Récupérer la position du robot|/01 get pos||@01 OK 0|
|4|Effectuer un déplacement du robot de 100 unités|/01 move 100||@01 OK 0|
|5|Attendre la fin du déplacement et récupérer à nouveau la position du robot|/01 get pos||@01 OK 100|
|6|Envoyer une commande « get » incomplète|/01 get||@01 RJ 0|
|7|Envoyer une mauvaise commande « get »|/01 get status||@01 RJ 0|

# Cas de test N°3 : Commande « set »

**Description :**

Vérifier le bon fonctionnement de la commande « set » et la détermination de la vitesse du robot

**Besoins :**

Robot alimenté et connecté au PC, l'identifiant du robot doit être configuré à 1, la liaison série est configurée et fonctionnelle, un seul robot doit être actif, la vitesse du robot doit être à 1

| Étape | Description | Commande | Réponse reçue | Réponse attendue |
|-------|-------------|----------|---------------|------------------|
|1|Récupérer la vitesse du robot|/01 get speed||@01 OK 1|
|2|Déterminer la vitesse du robot à 8|/01 set speed 8||@01 OK 0|
|3|Vérifier la vitesse du robot|/01 get speed||@01 OK 8|
|4|Envoyer une valeur de vitesse supérieure à la limite (>10)|/01 set speed 11||@01 RJ 0|
|5|Vérifier que la vitesse du robot n’a pas été changé|/01 get speed||@01 OK 8|
|6|Envoyer une valeur de vitesse inférieure à la limite (<1)|/01 set speed 0||@01 RJ 0|
|7|Vérifier que la vitesse du robot n’a pas été changé|/01 get speed||@01 OK 8|
|8|Envoyer une commande « set » incomplète (sans argument « speed »)|/01 set 5||@01 RJ 0|
|9|Envoyer une commande « set » incomplète (sans la valeur)|/01 set speed||@01 RJ 0|
|10|Envoyer une valeur de vitesse négative|/01 set speed -3||@01 RJ 0|
|11|Envoyer une valeur de vitesse en décimal|/01 set speed 3,5||@01 RJ 0|
|12|Vérifier que la vitesse du robot n’a pas changé|/01 get speed||@01 OK 8|

# Cas de test N°4 : Commande « move »

**Description :**

Vérifier le bon fonctionnement de la commande « move » et du déplacement du robot

**Besoins :**

Robot alimenté et connecté au PC, l'identifiant du robot doit être configuré à 1, la liaison série est configurée et fonctionnelle, un seul robot doit être actif, la position du robot doit être à 0

| Étape | Description | Commande | Réponse reçue | Réponse attendue |
|-------|-------------|----------|---------------|------------------|
|1|Récupérer la position du robot|/01 get pos||@01 OK 0|
|2|Déterminer la vitesse du robot à 1|/01 set speed 1||@01 OK 0|
|3|Vérifier la vitesse du robot|/01 get speed||@01 OK 1|
|4|Déplacer le robot de 15 unités vers l’avant|/01 move 15||@01 OK 0|
|5|Attendre 15 secondes et vérifier la position|/01 get pos||@01 OK 15|
|6|Déplacer le robot de 35 unités vers l’arrière|/01 move -35||@01 OK 0|
|7|Attendre 35 secondes et vérifier la position|/01 get pos||@01 OK -20|
|8|Déplacer le robot de 50 unités vers l’avant|/01 move 50||@01 OK 0|
|9|Sans attendre la fin du déplacement, Déplacer le robot de 60 unités vers l’avant|/01 move 60||@01 OK 0|
|10|Attendre 1min50 depuis l’étape 8 et vérifier la position|/01 get pos||@01 OK 90|
|11|Envoyer une valeur de déplacement incorrecte|/01 move 10,6||@01 RJ 0|
|12|Envoyer une commande incomplète|/01 move||@01 RJ 0|
|13|Vérifier que la position du robot n’a pas changé|/01 get pos||@01 OK 90|
|14|Envoyer une commande avec une valeur trop élevé|/01 move 9999999999999||@01 RJ 0|


# Cas de test N°5 : Vérification du déplacement

**Description :**

Vérifier le bon fonctionnement de déplacement du robot en variant la vitesse et ainsi le temps de déplacement

**Besoins :**

Robot alimenté et connecté au PC, l'identifiant du robot doit être configuré à 1, la liaison série est configurée et fonctionnelle, un seul robot doit être actif, les valeurs du robot sont réinitialisées (vitesse à 1 et position à 0)

| Étape | Description | Commande | Réponse reçue | Réponse attendue |
|-------|-------------|----------|---------------|------------------|
|1|Déplacer le robot de 50 unités vers l’avant|/01 move 45||@01 OK 0|
|2|Attendre 15 secondes et vérifier la position du robot|/01 get pos||@01 OK 15|
|3|Attendre 35 secondes et vérifier la position du robot|/01 get pos||@01 OK 50|
|4|Définir la vitesse du robot à 5|/01 set speed 5||@01 OK0|
|5|Déplacer le robot de 500 unités vers l’avant|/01 move 500||@01 OK 0|
|6|Attendre 10 secondes et vérifier la position du robot|/01 get pos||@01 OK 100|
|7|Attendre 1min30 et vérifier la position du robot|/01 get pos||@01 OK 550|
|8|Définir la vitesse du robot à 2|/01 set speed 2||@01 OK 0|
|9|Déplacer le robot de 550 unités vers l’arrière|/01 move -550||@01 OK 0|
|10|Attendre 60 secondes et vérifier la position du robot|/01 get pos||@01 OK 430|
|11|Attendre 3min35 secondes et vérifier la position du robot|/01 get pos||@01 OK 0|

