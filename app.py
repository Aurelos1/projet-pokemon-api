
import streamlit as st

from pokemon import (
    obtenir_pokemon,
    obtenir_pokemon_par_type,
    calculer_moyenne_hp
)

st.set_page_config(
    page_title="Pokémon Explorer",
    page_icon="⚡",
    layout="wide"
)


# Mise en cache des calculs pendant une heure

@st.cache_data(ttl=3600)
def analyser_hp_en_cache(noms):
    return calculer_moyenne_hp(noms)


st.title("⚡ Pokémon Explorer")

onglet_recherche, onglet_comparaison, onglet_types, onglet_combat = st.tabs([
    "🔍 Rechercher",
    "⚔️ Comparaison",
    "🔥 Analyse par type",
    "🥊 Combat"
])


# ==========================================
# ONGLET 1 : RECHERCHE
# ==========================================

with onglet_recherche:
    st.subheader("🔍 Rechercher un Pokémon")

    nom = st.text_input(
        "Nom ou ID du Pokémon",
        value="pikachu"
    )

    if st.button("Rechercher"):
        if not nom.strip():
            st.warning("Entre un nom ou un ID.")
        else:
            try:
                pokemon = obtenir_pokemon(nom)

                if pokemon is None:
                    st.error("Pokémon introuvable.")
                else:
                    st.success("Pokémon trouvé !")
                    st.subheader(pokemon["name"].capitalize())

                    image = pokemon["sprites"]["front_default"]
                    if image:
                        st.image(image)

                    st.write("**ID :**", pokemon["id"])
                    st.write("**Taille :**", pokemon["height"] / 10, "m")
                    st.write("**Poids :**", pokemon["weight"] / 10, "kg")

                    st.write("### Statistiques")

                    for stat in pokemon["stats"]:
                        st.write(
                            f"{stat['stat']['name']} : "
                            f"{stat['base_stat']}"
                        )

            except Exception as erreur:
                st.error(str(erreur))


# ==========================================
# ONGLET 2 : COMPARAISON
# ==========================================

with onglet_comparaison:
    st.subheader("⚔️ Comparer deux Pokémon")

    col1, col2 = st.columns(2)

    with col1:
        nom1 = st.text_input(
            "Premier Pokémon",
            value="pikachu"
        )

    with col2:
        nom2 = st.text_input(
            "Deuxième Pokémon",
            value="charizard"
        )

    if st.button("Comparer"):
        if not nom1.strip() or not nom2.strip():
            st.warning("Entre deux noms.")
        else:
            try:
                p1 = obtenir_pokemon(nom1)
                p2 = obtenir_pokemon(nom2)

                if p1 is None or p2 is None:
                    st.error("Un des Pokémon est introuvable.")
                else:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader(p1["name"].capitalize())
                        image1 = p1["sprites"]["front_default"]
                        if image1:
                            st.image(image1)

                    with col2:
                        st.subheader(p2["name"].capitalize())
                        image2 = p2["sprites"]["front_default"]
                        if image2:
                            st.image(image2)

                    # Transformation des statistiques JSON en dictionnaire
                    # Exemple : {"hp": 35, "attack": 55, ...}
                    stats1 = {
                        s["stat"]["name"]: s["base_stat"]
                        for s in p1["stats"]
                    }

                    stats2 = {
                        s["stat"]["name"]: s["base_stat"]
                        for s in p2["stats"]
                    }

                    tableau = []
                    # Comparaison des statistiques pour identifier le meilleur Pokémon

                    for stat, valeur1 in stats1.items():
                        valeur2 = stats2[stat]

                        if valeur1 > valeur2:
                            meilleur = p1["name"].capitalize()
                        elif valeur2 > valeur1:
                            meilleur = p2["name"].capitalize()
                        else:
                            meilleur = "Égalité"

                        tableau.append({
                            "Statistique": stat,
                            p1["name"].capitalize(): valeur1,
                            p2["name"].capitalize(): valeur2,
                            "Meilleur": meilleur
                        })

                    st.write("### Comparaison des statistiques")
                    st.dataframe(tableau, hide_index=True)

                    st.write("### 🏆 Résultat")

                    for stat, titre in [
                        ("hp", "❤️ Points de vie"),
                        ("attack", "⚔️ Attaque")
                    ]:
                        v1 = stats1[stat]
                        v2 = stats2[stat]

                        if v1 > v2:
                            gagnant = p1["name"].capitalize()
                        elif v2 > v1:
                            gagnant = p2["name"].capitalize()
                        else:
                            gagnant = "Égalité"

                        st.write(
                            f"**{titre} : {gagnant}** "
                            f"({v1} contre {v2})"
                        )

            except Exception as erreur:
                st.error(str(erreur))


# ==========================================
# ONGLET 3 : ANALYSE PAR TYPE
# ==========================================

with onglet_types:
    st.subheader("🔥 Analyse des Pokémon par type")

    types = {
        "Feu 🔥": "fire",
        "Eau 💧": "water",
        "Plante 🌿": "grass",
        "Électrik ⚡": "electric",
        "Psy 🔮": "psychic",
        "Dragon 🐉": "dragon"
    }

    choix = st.selectbox(
        "Choisis un type",
        list(types.keys())
    )

    if st.button("Analyser ce type"):
        try:
            with st.spinner("Récupération du type..."):
                noms = obtenir_pokemon_par_type(types[choix])

            st.metric(
                "Nombre de Pokémon associés à ce type",
                len(noms)
            )

            st.write("### Quelques Pokémon")
            for nom_pokemon in noms[:15]:
                st.write("•", nom_pokemon.capitalize())

            st.write("### 📊 Moyenne des HP")

            
            noms_a_analyser = tuple(noms[20])

            with st.spinner("Calcul des HP en cours..."):
                moyenne, nombre = analyser_hp_en_cache(
                    noms_a_analyser
                )

            if moyenne is not None:
                st.metric(
                    "Moyenne des HP des 20 premières entrées",
                    moyenne
                )
                st.caption(
                    f"{nombre} entrées analysées sur "
                    f"{len(noms)} au total."
                )
            else:
                st.warning("Aucune donnée HP disponible.")

        except Exception as erreur:
            st.error(f"Erreur pendant l'analyse : {erreur}")


# ==========================================
# ONGLET 4 : COMBAT POKÉMON
# ==========================================

with onglet_combat:
    st.subheader("🥊 Simulateur de combat Pokémon")

    st.write(
        "Simulation simplifiée sur 5 tours, "
        "basée sur l'attaque et la défense."
    )

    col1, col2 = st.columns(2)

    with col1:
        combattant1 = st.text_input(
            "Pokémon 1",
            value="pikachu"
        )

    with col2:
        combattant2 = st.text_input(
            "Pokémon 2",
            value="charizard"
        )

    if st.button("⚔️ Lancer le combat"):
        if not combattant1.strip() or not combattant2.strip():
            st.warning("Entre les noms des deux Pokémon.")
        else:
            try:
                p1 = obtenir_pokemon(combattant1)
                p2 = obtenir_pokemon(combattant2)

                if p1 is None or p2 is None:
                    st.error("Un des Pokémon est introuvable.")
                else:
                    stats1 = {
                        s["stat"]["name"]: s["base_stat"]
                        for s in p1["stats"]
                    }

                    stats2 = {
                        s["stat"]["name"]: s["base_stat"]
                        for s in p2["stats"]
                    }
                    # Calcul simplifié des dégâts selon l'attaque et la défense adverse

                    degats1 = max(
                        1,
                        int(
                            stats1["attack"]
                            - stats2["defense"] / 2
                        )
                    )

                    degats2 = max(
                        1,
                        int(
                            stats2["attack"]
                            - stats1["defense"] / 2
                        )
                    )

                    total1 = 0
                    total2 = 0
                    tours = []

                    # Simulation de cinq tours et cumul des dégâts
                    for tour in range(1, 6):
                        total1 += degats1
                        total2 += degats2

                        tours.append({
                            "Tour": tour,
                            p1["name"].capitalize(): degats1,
                            p2["name"].capitalize(): degats2
                        })

                    st.write("### Résultats des 5 tours")
                    st.dataframe(tours, hide_index=True)

                    st.write("### Dégâts totaux")

                    st.write(
                        f"**{p1['name'].capitalize()} :** {total1}"
                    )
                    st.write(
                        f"**{p2['name'].capitalize()} :** {total2}"
                    )

                    if total1 > total2:
                        gagnant = p1["name"].capitalize()
                    elif total2 > total1:
                        gagnant = p2["name"].capitalize()
                    else:
                        gagnant = "Égalité"

                    st.success(
                        f"🏆 Résultat du combat : {gagnant}"
                    )

            except Exception as erreur:
                st.error(str(erreur))
