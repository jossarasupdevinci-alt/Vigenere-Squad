
from math import gcd


def valider_cle(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Les cles doivent etre des entiers.")

    if gcd(a, 26) != 1:
        raise ValueError("La cle a doit etre premiere avec 26.")

    return a, b


def chiffrer_affine(message, a, b):
    valider_cle(a, b)
    resultat = ""

    for lettre in message.upper():
        if lettre.isascii() and lettre.isalpha():
            x = ord(lettre) - ord("A")
            y = (a * x + b) % 26
            resultat += chr(y + ord("A"))
        else:
            resultat += lettre

    return resultat


def dechiffrer_affine(message, a, b):
    valider_cle(a, b)

    inverse_a = pow(a, -1, 26)
    resultat = ""

    for lettre in message.upper():
        if lettre.isascii() and lettre.isalpha():
            y = ord(lettre) - ord("A")
            x = (inverse_a * (y - b)) % 26
            resultat += chr(x + ord("A"))
        else:
            resultat += lettre

    return resultat


if __name__ == "__main__":
    message = "BONJOUR"
    a = 5
    b = 8

    chiffre = chiffrer_affine(message, a, b)
    dechiffre = dechiffrer_affine(chiffre, a, b)

    print("Message original :", message)
    print("Message chiffre :", chiffre)
    print("Message dechiffre :", dechiffre)
