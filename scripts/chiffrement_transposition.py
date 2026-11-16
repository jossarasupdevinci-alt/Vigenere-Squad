
def valider_cle(cle):
    """Vérifie que la clé est non vide et composée de lettres A-Z."""
    if not isinstance(cle, str) or not cle:
        raise ValueError("La clé ne doit pas être vide.")

    cle = cle.upper()

    if not cle.isascii() or not cle.isalpha():
        raise ValueError("La clé doit contenir uniquement des lettres A-Z.")

    return cle


def obtenir_ordre_colonnes(cle):
    """Détermine l'ordre des colonnes, même si la clé contient des doublons."""
    return sorted(range(len(cle)), key=lambda i: (cle[i], i))


def chiffrer_transposition(message, cle):
    """Chiffre un message par transposition en colonnes."""
    cle = valider_cle(cle)
    nombre_colonnes = len(cle)
    resultat = []

    for colonne in obtenir_ordre_colonnes(cle):
        for position in range(colonne, len(message), nombre_colonnes):
            resultat.append(message[position])

    return "".join(resultat)


def dechiffrer_transposition(message, cle):
    """Déchiffre un message par transposition en colonnes."""
    cle = valider_cle(cle)

    nombre_colonnes = len(cle)
    longueur = len(message)

    if longueur == 0:
        return ""

    nombre_lignes = (longueur + nombre_colonnes - 1) // nombre_colonnes
    colonnes_longues = longueur % nombre_colonnes

    if colonnes_longues == 0:
        colonnes_longues = nombre_colonnes

    colonnes = [""] * nombre_colonnes
    position = 0

    for colonne in obtenir_ordre_colonnes(cle):
        taille = nombre_lignes if colonne < colonnes_longues else nombre_lignes - 1
        colonnes[colonne] = message[position:position + taille]
        position += taille

    resultat = []

    for ligne in range(nombre_lignes):
        for colonne in range(nombre_colonnes):
            if ligne < len(colonnes[colonne]):
                resultat.append(colonnes[colonne][ligne])

    return "".join(resultat)
