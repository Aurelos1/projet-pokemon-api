
import time
import requests
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor


# Cache des données pendant 1 heure
cache = {}
DUREE_CACHE = 3600


def requete_api(url, max_tentatives=2):
    maintenant = time.time()

    # Vérifier si la réponse est déjà en cache
    if url in cache:
        donnees, expiration = cache[url]

        if maintenant < expiration:
            return donnees

        del cache[url]

    # Appel API avec tentatives automatiques
    for tentative in range(max_tentatives):
        try:
            reponse = requests.get(url, timeout=5)

            if reponse.status_code == 200:
                donnees = reponse.json()
                cache[url] = (
                    donnees,
                    time.time() + DUREE_CACHE
                )
                return donnees

            if reponse.status_code == 404:
                return None

            if reponse.status_code in (429, 500, 503):
                if tentative < max_tentatives - 1:
                    time.sleep(1)
                    continue

            reponse.raise_for_status()

        except requests.exceptions.RequestException:
            if tentative == max_tentatives - 1:
                raise

            time.sleep(1)

    return None


def obtenir_pokemon(nom):
    nom = str(nom).strip().lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{nom}"
    return requete_api(url)


def obtenir_pokemon_par_type(type_pokemon):
    url = f"https://pokeapi.co/api/v2/type/{type_pokemon}"
    donnees = requete_api(url)

    if donnees is None:
        return []

    return [
        element["pokemon"]["name"]
        for element in donnees["pokemon"]
    ]


def calculer_moyenne_hp(noms):

    def recuperer_hp(nom):
        try:
            pokemon = obtenir_pokemon(nom)

            if pokemon is None:
                return None

            for statistique in pokemon["stats"]:
                if statistique["stat"]["name"] == "hp":
                    return statistique["base_stat"]

        except requests.exceptions.RequestException:
            return None

        return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        resultats = list(executor.map(recuperer_hp, noms))

    valeurs_hp = [
        hp for hp in resultats
        if hp is not None
    ]

    if not valeurs_hp:
        return None, 0

    moyenne = sum(valeurs_hp) / len(valeurs_hp)

    return round(moyenne, 2), len(valeurs_hp)
