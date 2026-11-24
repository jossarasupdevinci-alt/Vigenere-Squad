
from collections import Counter
from math import gcd
from functools import reduce

from scripts.khi_deux import FREQUENCES_FR
from scripts.kasiski import analyser_kasiski
from scripts.chiffrement_vigenere import dechiffrer_vigenere
from scripts.score_quadgrammes import calculer_score_moyen


def nettoyer_message(message):
    return "".join(
        lettre for lettre in message.upper()
        if "A" <= lettre <= "Z"
    )


def calculer_ic(texte):
    if len(texte) < 2:
        return 0.0

    frequences = Counter(texte)
    longueur = len(texte)

    return sum(
        n * (n - 1) for n in frequences.values()
    ) / (longueur * (longueur - 1))


def estimer_longueurs_cle(message, longueur_max=16):
    scores = {}

    for longueur in range(1, min(longueur_max, len(message) // 2) + 1):
        colonnes = [
            message[i::longueur]
            for i in range(longueur)
        ]

        indices = [
            calculer_ic(colonne)
            for colonne in colonnes
            if len(colonne) >= 2
        ]

        scores[longueur] = (
            sum(indices) / len(indices)
            if indices else 0.0
        )

    # Analyse Kasiski : les facteurs des distances
    # donnent des indications sur la longueur de la clé.
    _, distances, _ = analyser_kasiski(message)

    votes = Counter()

    for distance in distances:
        for facteur in range(2, longueur_max + 1):
            if distance % facteur == 0:
                votes[facteur] += 1

    meilleurs_ic = sorted(
        scores,
        key=scores.get,
        reverse=True
    )[:8]

    meilleurs_kasiski = [
        longueur
        for longueur, _ in votes.most_common(8)
        if longueur in scores
    ]

    candidats = list(dict.fromkeys(
        meilleurs_ic + meilleurs_kasiski
    ))

    if not candidats:
        raise ValueError("Impossible d'estimer la longueur de clé.")

    return candidats, scores


def trouver_decalage(colonne):
    meilleur_decalage = 0
    meilleur_score = float("inf")

    total = len(colonne)

    if total == 0:
        return 0

    for decalage in range(26):
        score = 0.0

        for lettre, frequence in FREQUENCES_FR.items():
            observe = sum(
                1 for caractere in colonne
                if chr((ord(caractere) - 65 - decalage) % 26 + 65)
                == lettre
            )

            attendu = total * frequence / 100

            score += (observe - attendu) ** 2 / attendu

        if score < meilleur_score:
            meilleur_score = score
            meilleur_decalage = decalage

    return meilleur_decalage


def retrouver_cle(message, longueur):
    cle = ""

    for position in range(longueur):
        colonne = message[position::longueur]
        decalage = trouver_decalage(colonne)
        cle += chr(decalage + 65)

    return reduire_cle(cle)


def attaquer_vigenere(
    message,
    modele=None,
    longueur_max=16,
):
    texte = nettoyer_message(message)

    if len(texte) < 20:
        raise ValueError(
            "Le texte doit contenir au moins 20 lettres."
        )

    longueurs, scores_ic = estimer_longueurs_cle(
        texte,
        longueur_max
    )

    resultats = []

    for longueur in longueurs:
        cle = retrouver_cle(texte, longueur)
        texte_clair = dechiffrer_vigenere(texte, cle)

        score = (
            calculer_score_moyen(texte_clair, modele)
            if modele is not None
            else scores_ic[longueur]
        )

        resultats.append({
            "longueur_cle": longueur,
            "cle": cle,
            "texte_clair": texte_clair,
            "score": score,
            "indice_coincidence": scores_ic[longueur],
        })

    resultats.sort(
        key=lambda resultat: resultat["score"],
        reverse=True
    )

    meilleur = resultats[0]

    return {
        **meilleur,
        "candidats": resultats,
    }
def reduire_cle(cle):
    for longueur in range(1, len(cle) + 1):
        candidate = cle[:longueur]
        if candidate * (len(cle) // longueur) + candidate[:len(cle) % longueur] == cle:
            return candidate
    return cle
