
from collections import Counter
import string


def nettoyer_message(message):
    return "".join(
        lettre for lettre in message.upper()
        if lettre in string.ascii_uppercase
    )


def analyser_frequences(message):
    texte = nettoyer_message(message)

    if not texte:
        raise ValueError("Le message ne contient aucune lettre A-Z.")

    compteur = Counter(texte)
    total = len(texte)

    frequences = {}

    for lettre in string.ascii_uppercase:
        nombre = compteur.get(lettre, 0)
        frequences[lettre] = round(nombre / total * 100, 2)

    return frequences


# Programme principal
if __name__ == "__main__":
    message = "BONJOUR BONJOUR"

    resultats = analyser_frequences(message)

    print("Analyse frequentielle :")
    for lettre, frequence in resultats.items():
        if frequence > 0:
            print(f"{lettre} : {frequence}%")
