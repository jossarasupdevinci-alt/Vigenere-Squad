
import string


ALPHABET = string.ascii_uppercase


def valider_cle(cle):
    cle = cle.upper()

    if len(cle) != 26:
        raise ValueError("La cle doit contenir exactement 26 lettres.")

    if not cle.isascii() or not cle.isalpha():
        raise ValueError("La cle doit contenir uniquement des lettres A-Z.")

    if len(set(cle)) != 26:
        raise ValueError("Chaque lettre de la cle doit etre unique.")

    return cle


def chiffrer_substitution(message, cle):
    cle = valider_cle(cle)
    resultat = ""

    for lettre in message.upper():
        if lettre in ALPHABET:
            position = ALPHABET.index(lettre)
            resultat += cle[position]
        else:
            resultat += lettre

    return resultat


def dechiffrer_substitution(message, cle):
    cle = valider_cle(cle)
    resultat = ""

    for lettre in message.upper():
        if lettre in cle:
            position = cle.index(lettre)
            resultat += ALPHABET[position]
        else:
            resultat += lettre

    return resultat


if __name__ == "__main__":
    message = "BONJOUR"
    cle = "QWERTYUIOPASDFGHJKLZXCVBNM"

    chiffre = chiffrer_substitution(message, cle)
    dechiffre = dechiffrer_substitution(chiffre, cle)

    print("Message original :", message)
    print("Message chiffre :", chiffre)
    print("Message dechiffre :", dechiffre)
