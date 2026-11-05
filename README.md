# ⚡ Pokémon Explorer — Mini-Projet 2

Ce projet est une application Python qui utilise **PokéAPI** pour récupérer des informations sur les Pokémon.

J'ai utilisé **Streamlit** pour créer une interface simple avec plusieurs fonctionnalités : rechercher un Pokémon, comparer ses statistiques avec un autre, analyser les Pokémon par type et simuler un combat.

## Comment fonctionne mon code ?

Le projet est séparé en trois fichiers Python :

- `app.py` : contient l'interface Streamlit et les quatre onglets.
- `pokemon.py` : permet de récupérer les données depuis PokéAPI et de faire les calculs.
- `questions_communes.py` : contient les exercices sur les requêtes HTTP, `asyncio` et le cache.

Dans mon code, j'utilise des boucles `for` pour parcourir les statistiques des Pokémon, afficher des listes et simuler les cinq tours d'un combat.

Les conditions `if`, `elif` et `else` permettent de vérifier les résultats et de comparer les Pokémon.

J'utilise aussi `try / except` pour gérer les erreurs et éviter que l'application s'arrête lorsqu'une requête échoue.

### Le fichier `pokemon.py`

Ce fichier regroupe les fonctions qui communiquent avec PokéAPI.

La fonction `requete_api()` envoie les requêtes HTTP. Elle vérifie d'abord si les données sont déjà dans le cache. Si ce n'est pas le cas, elle interroge l'API.

J'ai ajouté un délai d'attente (*timeout*) et un système de nouvelles tentatives pour certaines erreurs, comme les erreurs 429, 500 et 503.

Les fonctions `obtenir_pokemon()` et `obtenir_pokemon_par_type()` permettent de récupérer un Pokémon par son nom ou son ID, ou de récupérer la liste des Pokémon d'un type.

Enfin, `calculer_moyenne_hp()` récupère les points de vie des Pokémon et calcule leur moyenne. J'utilise `ThreadPoolExecutor` pour pouvoir récupérer plusieurs résultats en même temps, avec un maximum de cinq requêtes simultanées.

Le cache conserve les réponses pendant **une heure**, ce qui évite de refaire les mêmes appels à l'API.

## Technologies utilisées

- **Python** : langage utilisé pour le projet
- **Streamlit** : création de l'interface
- **Requests** : envoi des requêtes HTTP
- **PokéAPI** : récupération des données Pokémon
- **asyncio** : simulation de plusieurs requêtes en parallèle
- **ThreadPoolExecutor** : récupération simultanée de plusieurs Pokémon

## Fonctionnalités

### 1. Recherche de Pokémon

On peut rechercher un Pokémon avec son nom ou son identifiant.

L'application affiche son image, son ID, sa taille, son poids et ses principales statistiques (HP, attaque, défense, vitesse, etc.).

### 2. Comparaison de deux Pokémon

On entre les noms de deux Pokémon et l'application affiche leurs statistiques dans un tableau.

Elle indique également lequel possède le plus de **HP** et lequel possède la meilleure **attaque**.

### 3. Analyse par type

On peut sélectionner un type de Pokémon, par exemple Feu, Eau, Plante ou Dragon.

L'application affiche le nombre de Pokémon associés à ce type, quelques noms et une moyenne de leurs HP.

**Limite actuelle :** pour éviter des temps de chargement trop longs, je calcule la moyenne uniquement sur les **5 premiers Pokémon** de la liste, et non sur tous les Pokémon du type.

### 4. Simulation de combat

J'ai ajouté un petit simulateur de combat entre deux Pokémon.

Le combat dure **5 tours**. Les dégâts sont calculés à partir de l'attaque du Pokémon et de la défense de son adversaire.

La formule utilisée est :

`dégâts = max(1, int(attaque - défense_adverse / 2))`

Une boucle `for` permet de répéter le calcul pendant cinq tours et d'additionner les dégâts.

À la fin, le Pokémon qui a infligé le plus de dégâts gagne.

Il s'agit d'une simulation simplifiée, pas d'un vrai système de combat Pokémon.

## Questions communes

### Q1 — Gestion des erreurs HTTP

Dans `questions_communes.py`, j'ai créé une fonction `requete_api_robuste()` pour mieux gérer les appels à une API.

Elle permet notamment de :

- Gérer les erreurs HTTP comme 400, 401, 403, 404, 429, 500 et 503.
- Définir un délai d'attente pour les réponses.
- Réessayer jusqu'à trois fois lorsqu'une erreur temporaire se produit.
- Utiliser `time.sleep()` pour attendre entre les tentatives.

### Q2 — Simulation avec asyncio

Pour cette question, j'ai utilisé `asyncio` afin de simuler plusieurs appels vers trois routes fictives :

- `https://api.example.com/data1`
- `https://api.example.com/data2`
- `https://api.example.com/data3`

J'ai utilisé `asyncio.gather()` pour exécuter les tâches de manière concurrente et `asyncio.Semaphore(100)` pour limiter le nombre de tâches simultanées.

Lors de mon test, **1 000 requêtes simulées ont pris environ 1,12 seconde**.

Les appels sont simulés avec `asyncio.sleep()` : il n'y a donc pas de vraies requêtes HTTP vers ces adresses. Cette partie montre le principe de la concurrence, mais ne teste pas réellement un million de requêtes.

### Q3 — Cache d'une heure

J'ai créé un cache avec un dictionnaire Python. Les données restent valides pendant **3 600 secondes**, soit une heure.

Pour vérifier son fonctionnement, j'ai testé trois situations :

1. Un premier appel récupère les données depuis l'API.
2. Un deuxième appel réutilise les données déjà en cache.
3. Après avoir simulé l'expiration du cache, un nouvel appel est effectué.

## Installation

Pour récupérer le projet :

```bash
git clone https://github.com/Aurelos1/projet-pokemon-api.git
cd projet-pokemon-api
```

Installer les bibliothèques nécessaires :

```bash
python -m pip install -r requirements.txt
```

## Lancer l'application

Dans le terminal :

```bash
python -m streamlit run app.py
```

L'application s'ouvre normalement dans le navigateur à l'adresse :

`http://localhost:8501`

## Tester les questions communes

Pour exécuter les exercices Q1, Q2 et Q3 :

```bash
python questions_communes.py
```

## Organisation du projet

```text
projet-pokemon-api/
├── app.py
├── pokemon.py
├── questions_communes.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API utilisée

Documentation de PokéAPI : https://pokeapi.co/

Les deux routes principales utilisées sont :

- `/api/v2/pokemon/{id}` : informations sur un Pokémon
- `/api/v2/type/{type}` : Pokémon associés à un type