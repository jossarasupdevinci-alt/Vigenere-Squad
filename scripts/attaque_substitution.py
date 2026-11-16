
import random
import string
import re
import math
from pathlib import Path

from scripts.score_quadgrammes import charger_modele, calculer_score_moyen

ALPHABET = string.ascii_uppercase


def generer_cle_aleatoire():
    lettres = list(ALPHABET)
    random.shuffle(lettres)
    return "".join(lettres)


def modifier_cle(cle):
    lettres = list(cle)
    p1, p2 = random.sample(range(26), 2)
    lettres[p1], lettres[p2] = lettres[p2], lettres[p1]
    return "".join(lettres)


def chiffrer_substitution(message, cle):
    resultat = []
    for caractere in message.upper():
        if caractere in ALPHABET:
            resultat.append(cle[ord(caractere) - ord("A")])
        else:
            resultat.append(caractere)
    return "".join(resultat)


def dechiffrer_substitution(message, cle):
    resultat = []
    for caractere in message.upper():
        if caractere in ALPHABET:
            resultat.append(ALPHABET[cle.index(caractere)])
        else:
            resultat.append(caractere)
    return "".join(resultat)


def evaluer_cle(message, cle, modele):
    texte = dechiffrer_substitution(message, cle)
    return calculer_score_moyen(texte, modele)


def recuit_simule(
    message,
    modele,
    iterations=100000,
    temperature_initiale=20,
    refroidissement=0.9999,
    graine=42
):
    random.seed(graine)

    cle_actuelle = generer_cle_aleatoire()
    texte_actuel = dechiffrer_substitution(message, cle_actuelle)
    score_actuel = calculer_score_moyen(texte_actuel, modele)

    meilleure_cle = cle_actuelle
    meilleur_texte = texte_actuel
    meilleur_score = score_actuel
    temperature = temperature_initiale

    for _ in range(iterations):
        nouvelle_cle = modifier_cle(cle_actuelle)
        nouveau_texte = dechiffrer_substitution(message, nouvelle_cle)
        nouveau_score = calculer_score_moyen(nouveau_texte, modele)

        difference = nouveau_score - score_actuel

        if difference > 0 or (
            temperature > 0
            and random.random() < math.exp(difference / temperature)
        ):
            cle_actuelle = nouvelle_cle
            score_actuel = nouveau_score
            texte_actuel = nouveau_texte

        if score_actuel > meilleur_score:
            meilleure_cle = cle_actuelle
            meilleur_texte = texte_actuel
            meilleur_score = score_actuel

        temperature *= refroidissement

    return meilleure_cle, meilleur_texte, meilleur_score


def charger_texte_test():
    chemin = Path("data/corpus_francais.txt")
    texte = chemin.read_text(encoding="utf-8").upper()
    texte = re.sub(r"[^A-Z]", "", texte)

    if len(texte) < 1000:
        raise ValueError("Le corpus doit contenir au moins 1000 lettres.")

    return texte[:1000]


if __name__ == "__main__":
    modele = charger_modele()
    texte_original = charger_texte_test()

    cle_secrete = "QWERTYUIOPASDFGHJKLZXCVBNM"
    message_chiffre = chiffrer_substitution(texte_original, cle_secrete)

    print("Longueur du texte :", len(texte_original))
    print("Texte chiffre :", message_chiffre[:100], "...")

    print("\nAttaque en cours...")

    cle, texte, score = recuit_simule(
        message_chiffre,
        modele,
        iterations=100000,
        graine=42
    )

    exactitude = sum(
        a == b for a, b in zip(texte_original, texte)
    ) / len(texte_original) * 100

    print("\n--- RESULTAT DE L'ATTAQUE ---")
    print("Cle secrete :", cle_secrete)
    print("Cle trouvee :", cle)
    print("Score moyen :", round(score, 4))
    print("Exactitude :", round(exactitude, 2), "%")
    print("\nTexte original :", texte_original[:200])
    print("Texte dechiffre :", texte[:200])
