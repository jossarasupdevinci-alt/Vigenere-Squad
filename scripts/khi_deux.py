
from collections import Counter
import string

# Frequences approximatives des lettres en francais (%)
FREQUENCES_FR = {
    "A": 7.6, "B": 0.9, "C": 3.3, "D": 3.7,
    "E": 14.7, "F": 1.1, "G": 1.0, "H": 0.7,
    "I": 7.5, "J": 0.6, "K": 0.1, "L": 5.5,
    "M": 3.0, "N": 7.1, "O": 5.8, "P": 2.5,
    "Q": 1.4, "R": 6.6, "S": 7.9, "T": 7.2,
    "U": 6.3, "V": 1.6, "W": 0.1, "X": 0.4,
    "Y": 0.3, "Z": 0.1
}


def calculer_khi_deux(message):
    texte = "".join(
        lettre for lettre in message.upper()
        if lettre in string.ascii_uppercase
    )

    if not texte:
        raise ValueError("Le message ne contient aucune lettre A-Z.")

    compteur = Counter(texte)
    total = len(texte)
    score = 0

    for lettre, frequence in FREQUENCES_FR.items():
        observe = compteur.get(lettre, 0)
        attendu = total * frequence / 100

        score += (observe - attendu) ** 2 / attendu

    return score


if __name__ == "__main__":
    message = "BONJOUR BONJOUR BONJOUR"

    score = calculer_khi_deux(message)

    print("Message analyse :", message)
    print("Score Khi-deux :", round(score, 2))
