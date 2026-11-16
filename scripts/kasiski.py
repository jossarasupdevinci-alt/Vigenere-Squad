
from collections import Counter
from math import gcd
from functools import reduce


def trouver_repetitions(message, taille_min=3):
    positions = {}

    for taille in range(taille_min, len(message) // 2 + 1):
        for i in range(len(message) - taille + 1):
            groupe = message[i:i + taille]
            positions.setdefault(groupe, []).append(i)

    repetitions = {}

    for groupe, indices in positions.items():
        if len(indices) >= 2:
            repetitions[groupe] = indices

    return repetitions


def analyser_kasiski(message):
    texte = "".join(
        lettre for lettre in message.upper()
        if lettre.isascii() and lettre.isalpha()
    )

    repetitions = trouver_repetitions(texte)

    distances = []

    for indices in repetitions.values():
        for i in range(len(indices) - 1):
            distances.append(indices[i + 1] - indices[i])

    if not distances:
        return repetitions, distances, None

    pgcd = reduce(gcd, distances)

    return repetitions, distances, pgcd


if __name__ == "__main__":
    message = "ABCXYZABCXYZABCXYZ"

    repetitions, distances, pgcd = analyser_kasiski(message)

    print("Message chiffre :", message)
    print("Repetitions :", repetitions)
    print("Distances :", distances)
    print("PGCD des distances :", pgcd)
