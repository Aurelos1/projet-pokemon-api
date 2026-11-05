
import time
import requests
from concurrent.futures import ThreadPoolExecutor


# Cache des données pendant 1 heure
cache = {}
DUREE_CACHE = 3600


def requete_api(url, max_tentatives=2):
    maintenant = time.time()

    # Vérifier si la réponse est déjà en cache, si expiré, les supprimes
    #evite de refaire les memes requetes et rend la tache plus rapide
    if url in cache:
        donnees, expiration = cache[url]

        if maintenant < expiration:
            return donnees

        del cache[url]

    # Appel API avec tentatives automatiques
    #Cette boucle permet de réessayer une requête HTTP. Avec max_tentatives=2, elle peut effectuer deux essais maximum.
    # Si PokéAPI renvoie une erreur temporaire (429, 500, 503), le programme attend une seconde avec time.sleep(1) avant de réessayer.
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
    # Elle parcourt tous les Pokémon retournés par l'API et récupère uniquement leurs noms. exp : Charmelon,charizard...]
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
#boucle parcourant les stats des pokemons, cherche hp et la return
            for statistique in pokemon["stats"]:
                if statistique["stat"]["name"] == "hp":
                    return statistique["base_stat"]

        except requests.exceptions.RequestException:
            return None

        return None
#Sans cette instruction, Python récupérerait les HP des Pokémon un par un.; ThreadPoolExecutor en traite plusieurs
    with ThreadPoolExecutor(max_workers=5) as executor:
        resultats = list(executor.map(recuperer_hp, noms))

#Cette ligne conserve uniquement les HP récupérés avec succès.
    valeurs_hp = [
        hp for hp in resultats
        if hp is not None
    ]

    if not valeurs_hp:
        return None, 0
    #additione tous les HP/le nombre (len)
    moyenne = sum(valeurs_hp) / len(valeurs_hp)
    # la division donne la moyenne et return 2 résultats, ma moyenne arrondie et le nombre de Pokémon analysés 
    return round(moyenne, 2), len(valeurs_hp)
