
from collections import Counter
import string


def calculer_indice_coincidence(message):
    texte = "".join(
        lettre for lettre in message.upper()
        if lettre in string.ascii_uppercase
    )

    longueur = len(texte)

    if longueur < 2:
        raise ValueError("Le message doit contenir au moins deux lettres.")

    frequences = Counter(texte)

    numerateur = sum(
        nombre * (nombre - 1)
        for nombre in frequences.values()
    )

    denominateur = longueur * (longueur - 1)

    return numerateur / denominateur


if __name__ == "__main__":
    message = "BONJOUR BONJOUR"

    indice = calculer_indice_coincidence(message)

    print("Message :", message)
    print("Indice de coincidence :", round(indice, 4))
