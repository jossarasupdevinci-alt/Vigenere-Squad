

def valider_cle(cle):
    if not cle:
        raise ValueError("La cle ne peut pas etre vide.")

    cle = cle.upper()

    if not cle.isascii() or not cle.isalpha():
        raise ValueError("La cle doit contenir uniquement des lettres A-Z.")

    return cle

def chiffrer_vigenere(message, cle):
    resultat = ""
    cle = valider_cle(cle)
    index_cle = 0

    for lettre in message.upper():
        if lettre.isalpha() and lettre.isascii():
            position_message = ord(lettre) - ord("A")

            position_cle = ord(cle[index_cle % len(cle)]) - ord("A")

            nouvelle_position = (position_message + position_cle) % 26

            nouvelle_lettre = chr(nouvelle_position + ord("A"))

            resultat += nouvelle_lettre
            index_cle += 1
        else:
            resultat += lettre

    return resultat


def dechiffrer_vigenere(message, cle):
    resultat = ""
    cle = valider_cle(cle)
    index_cle = 0

    for lettre in message.upper():
        if lettre.isalpha() and lettre.isascii():
            position_message = ord(lettre) - ord("A")

            position_cle = ord(cle[index_cle % len(cle)]) - ord("A")

            nouvelle_position = (position_message - position_cle) % 26

            nouvelle_lettre = chr(nouvelle_position + ord("A"))

            resultat += nouvelle_lettre
            index_cle += 1
        else:
            resultat += lettre

    return resultat



# Programme principal
if __name__ == "__main__":
    message = "BONJOUR"
    cle = "CLE"

    message_chiffre = chiffrer_vigenere(message, cle)
    message_dechiffre = dechiffrer_vigenere(message_chiffre, cle)

    print("Message original :", message)
    print("Cle utilisee :", cle)
    print("Message chiffre :", message_chiffre)
    print("Message dechiffre :", message_dechiffre)

