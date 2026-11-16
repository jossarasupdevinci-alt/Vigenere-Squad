
import string


def force_brute_cesar(message):
    resultats = {}

    for cle in range(26):
        texte = ""

        for lettre in message.upper():
            if lettre in string.ascii_uppercase:
                position = ord(lettre) - ord("A")
                nouvelle_position = (position - cle) % 26
                texte += chr(nouvelle_position + ord("A"))
            else:
                texte += lettre

        resultats[cle] = texte

    return resultats


# Programme principal
if __name__ == "__main__":
    message_chiffre = "ERQMRXU"

    resultats = force_brute_cesar(message_chiffre)

    print("Message chiffre :", message_chiffre)
    print("\nLes 26 tentatives :")

    for cle, texte in resultats.items():
        print(f"Cle {cle:2} : {texte}")
