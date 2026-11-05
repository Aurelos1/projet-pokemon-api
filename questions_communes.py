
import asyncio
import time
import requests


# ==========================================
# Q1 : GESTION DES ERREURS ET RETRY
# ==========================================

def requete_api_robuste(url, max_tentatives=3):
    """
    Appel HTTP avec timeout, gestion des erreurs
    et nouvelles tentatives en cas d'erreur temporaire.
    """
    for tentative in range(1, max_tentatives + 1):
        try:
            reponse = requests.get(url, timeout=5)

            if reponse.status_code == 200:
                return reponse.json()

            if reponse.status_code == 404:
                print("Erreur 404 : ressource introuvable.")
                return None

            if reponse.status_code in (400, 401, 403):
                print(
                    f"Erreur client {reponse.status_code} : "
                    "requête ou autorisation invalide."
                )
                return None

            if reponse.status_code in (429, 500, 503):
                print(
                    f"Tentative {tentative}/{max_tentatives} : "
                    f"erreur temporaire {reponse.status_code}"
                )

                if tentative < max_tentatives:
                    time.sleep(2)
                    continue

                return None

            reponse.raise_for_status()

        except requests.exceptions.RequestException as erreur:
            print(f"Tentative {tentative} : {erreur}")

            if tentative < max_tentatives:
                time.sleep(2)
            else:
                return None

    return None


# ==========================================
# Q2 : SIMULATION DE FORTE CHARGE AVEC ASYNCIO
# ==========================================

ROUTES = [
    "https://api.example.com/data1",
    "https://api.example.com/data2",
    "https://api.example.com/data3"
]


async def appel_simule(url, semaphore):
    """
    Simulation d'un appel API.
    Aucun appel HTTP réel n'est effectué.
    """
    async with semaphore:
        await asyncio.sleep(0.1)
        return {"url": url, "statut": 200}


async def simuler_charge(nombre_requetes=1000):
    """
    Simule de nombreuses requêtes concurrentes
    avec un maximum de 100 tâches actives.
    """
    semaphore = asyncio.Semaphore(100)

    debut = time.perf_counter()

    taches = [
        appel_simule(
            ROUTES[i % len(ROUTES)],
            semaphore
        )
        for i in range(nombre_requetes)
    ]

    resultats = await asyncio.gather(*taches)

    duree = time.perf_counter() - debut

    print(f"Requêtes simulées : {len(resultats)}")
    print(f"Durée : {duree:.2f} secondes")
    print("Routes utilisées :", ", ".join(ROUTES))


# ==========================================
# Q3 : CACHE AVEC EXPIRATION D'UNE HEURE
# ==========================================

cache = {}
DUREE_CACHE = 3600


def requete_avec_cache(url):
    maintenant = time.time()

    if url in cache:
        donnees, expiration = cache[url]

        if maintenant < expiration:
            print("CACHE : données réutilisées.")
            return donnees

        print("CACHE : entrée expirée.")
        del cache[url]

    print("API : nouvelle requête.")
    donnees = requete_api_robuste(url)

    if donnees is not None:
        cache[url] = (
            donnees,
            time.time() + DUREE_CACHE
        )

    return donnees


# ==========================================
# DÉMONSTRATION DES 3 QUESTIONS
# ==========================================

if __name__ == "__main__":

    url_test = "https://pokeapi.co/api/v2/pokemon/pikachu"

    print("\n===== Q1 : REQUÊTE ROBUSTE =====")
    pokemon = requete_api_robuste(url_test)

    if pokemon:
        print("Pokémon récupéré :", pokemon["name"])

    print("\n===== Q2 : SIMULATION ASYNCIO =====")
    asyncio.run(simuler_charge(1000))

    print("\n===== Q3 : CACHE 1 HEURE =====")

    print("\nPremier appel :")
    requete_avec_cache(url_test)

    print("\nDeuxième appel :")
    requete_avec_cache(url_test)

    print("\nSimulation de l'expiration :")

    if url_test in cache:
        donnees, _ = cache[url_test]
        cache[url_test] = (
            donnees,
            time.time() - 1
        )

    print("\nTroisième appel après expiration :")
    requete_avec_cache(url_test)
