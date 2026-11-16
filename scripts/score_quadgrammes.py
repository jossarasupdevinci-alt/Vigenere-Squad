
import re
from pathlib import Path


def charger_modele(chemin="data/quadgrammes_fr.txt"):
    modele = {}

    with Path(chemin).open("r", encoding="utf-8") as fichier:
        for ligne in fichier:
            parties = ligne.split()

            if len(parties) == 2:
                quadgramme, score = parties
                modele[quadgramme] = float(score)

    if not modele:
        raise ValueError("Le modele de quadgrammes est vide.")

    return modele


def calculer_score(message, modele):
    texte = re.sub(r"[^A-Z]", "", message.upper())

    if len(texte) < 4:
        return float("-inf")

    score = 0.0

    for i in range(len(texte) - 3):
        quadgramme = texte[i:i + 4]
        score += modele.get(quadgramme, -10.0)

    return score


def calculer_score_moyen(message, modele):
    texte = re.sub(r"[^A-Z]", "", message.upper())

    if len(texte) < 4:
        return float("-inf")

    nombre = len(texte) - 3

    return calculer_score(texte, modele) / nombre


if __name__ == "__main__":
    modele = charger_modele()

    message = "BONJOUR TOUT LE MONDE"

    print("Message :", message)
    print("Score quadgrammes :", round(calculer_score(message, modele), 2))
    print("Nombre de quadgrammes dans le modele :", len(modele))
    print("Score de BONJOUR :", calculer_score("BONJOUR", modele))
    print("Score de TEXTE INCONNU :", calculer_score("TEXTE INCONNU", modele))

    print("\n--- Comparaison des scores moyens ---")

    exemples = [
        "BONJOUR TOUT LE MONDE",
        "TEXTE INCONNU",
        "QZXWJHFKLMPTRVBC",
    ]

    for exemple in exemples:
        score = calculer_score_moyen(exemple, modele)
        print(exemple, ":", round(score, 4))
