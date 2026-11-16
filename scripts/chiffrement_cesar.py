def chiffrer_cesar(message, cle):
    resultat = ""

    for lettre in message.upper():
        if lettre.isalpha() and lettre.isascii():
            position = ord(lettre) - ord("A")
            nouvelle_position = (position + cle) % 26
            nouvelle_lettre = chr(nouvelle_position + ord("A"))
            resultat += nouvelle_lettre
        else:
            resultat += lettre

    return resultat




def chiffrer_cesar(message, cle):
    resultat = ""

    for lettre in message.upper():
        if lettre.isalpha() and lettre.isascii():
            position = ord(lettre) - ord("A")
            nouvelle_position = (position + cle) % 26
            nouvelle_lettre = chr(nouvelle_position + ord("A"))
            resultat += nouvelle_lettre
        else:
            resultat += lettre

    return resultat


def dechiffrer_cesar(message, cle):
    return chiffrer_cesar(message, -cle)


# Programme principal
message = "XYZ"
cle = 3

message_chiffre = chiffrer_cesar(message, cle)
message_dechiffre = dechiffrer_cesar(message_chiffre, cle)

print("Message original :", message)
print("Message chiffre :", message_chiffre)
print("Message dechiffre :", message_dechiffre)
