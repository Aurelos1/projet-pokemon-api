# ⚡ Pokémon Explorer — Mini-Projet 2

Application Python utilisant l'API RESTful [PokéAPI](https://pokeapi.co/) pour explorer et comparer des Pokémon, analyser leurs statistiques et simuler des combats.


Mon application utilise Streamlit pour l'interface et PokéAPI pour récupérer les données. Les boucles for permettent de parcourir les statistiques, de comparer les Pokémon et de simuler cinq tours de combat. Les conditions if servent à vérifier les résultats et à désigner les gagnants. Enfin, j'utilise un cache pour limiter les appels répétitifs à l'API.


Pokemon.py :

Le fichier pokemon.py regroupe les fonctions qui communiquent avec PokéAPI.
La fonction requete_api() centralise les appels HTTP. Elle utilise un délai d'attente (timeout), gère les erreurs courantes et effectue de nouvelles tentatives en cas d'erreur temporaire. Un cache d'une heure permet de réutiliser les réponses déjà obtenues.
Les fonctions obtenir_pokemon() et obtenir_pokemon_par_type() construisent les URL nécessaires pour récupérer les informations d'un Pokémon ou la liste des Pokémon associés à un type.
Enfin, calculer_moyenne_hp() récupère les points de vie des Pokémon et calcule leur moyenne. Elle utilise ThreadPoolExecutor pour effectuer jusqu'à cinq requêtes simultanément et réduire le temps d'attente.
Les boucles for servent notamment à réessayer les appels HTTP, parcourir les données JSON et rechercher la statistique HP.

## Technologies utilisées

- Python
- Streamlit : interface web
- Requests : appels HTTP
- PokéAPI : données des Pokémon
- asyncio : simulation de requêtes concurrentes
- ThreadPoolExecutor : exécution concurrente de requêtes

## Fonctionnalités

### 1. Recherche de Pokémon
Recherche par nom ou identifiant et affichage des informations principales : image, ID, taille, poids et statistiques (HP, attaque, défense, etc.).

### 2. Comparaison
Comparaison des statistiques de deux Pokémon dans un tableau, avec identification du meilleur Pokémon en points de vie et en attaque.

### 3. Analyse par type
Récupération des Pokémon associés à un type (Feu, Eau, Plante, etc.), affichage de leur nombre et calcul d'une moyenne de HP.

**Limitation actuelle :** pour réduire les temps de chargement, la moyenne est calculée sur les 5 premières entrées du type, et non sur l'ensemble du type.

### 4. Simulation de combat
Simulation simplifiée de cinq tours entre deux Pokémon, à partir de leurs statistiques de base d'attaque et de défense.

Formule utilisée :

`dégâts = max(1, int(attaque - défense_adverse / 2))`

Le Pokémon qui inflige le plus de dégâts cumulés en cinq tours gagne.

## Questions communes

### Q1 — Gestion des erreurs

Le fichier `questions_communes.py` contient une fonction `requete_api_robuste()` avec :

- Gestion des erreurs HTTP 400, 401, 403, 404, 429, 500 et 503.
- Timeout pour éviter les attentes illimitées.
- Jusqu'à trois tentatives en cas d'erreur temporaire.
- Pauses avec `time.sleep()` entre les tentatives.

### Q2 — Concurrence avec asyncio

Simulation de 1 000 appels vers trois routes fictives :

- `https://api.example.com/data1`
- `https://api.example.com/data2`
- `https://api.example.com/data3`

Utilisation de `asyncio.gather()` et `asyncio.Semaphore(100)` pour gérer les tâches concurrentes.

**Résultat observé :** 1 000 requêtes simulées en environ 1,12 seconde.

Les appels sont simulés avec `asyncio.sleep()` : aucune requête HTTP réelle n'est envoyée aux trois routes. Cette démonstration illustre la concurrence, sans constituer un test réel à un million de requêtes.

### Q3 — Cache d'une heure

Implémentation d'un cache Python avec une durée de validité de 3 600 secondes.

La démonstration montre :

1. Un premier appel à l'API.
2. Un deuxième appel utilisant les données en cache.
3. Une expiration simulée du cache.
4. Un nouvel appel à l'API après expiration.

## Installation

Cloner le dépôt :

```bash
git clone URL_DU_DEPOT
cd projet_poke
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

## Lancer l'application

```bash
python -m streamlit run app.py
```

L'application est accessible à l'adresse locale indiquée par Streamlit, généralement `http://localhost:8501`.

## Tester les questions communes

```bash
python questions_communes.py
```

## Organisation du projet

```text
projet_poke/
├── app.py
├── pokemon.py
├── questions_communes.py
├── requirements.txt
├── .gitignore
└── README.md
```

## API utilisée

PokéAPI : https://pokeapi.co/

Endpoints principaux :

- `/api/v2/pokemon/{id}`
- `/api/v2/type/{type}`

Projet réalisé dans le cadre d'un exercice pédagogique sur les API RESTful en Python.