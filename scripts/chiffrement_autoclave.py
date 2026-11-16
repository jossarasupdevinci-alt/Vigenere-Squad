
def valider_cle(cle):
    """Vérifie que la clé contient uniquement des lettres A-Z."""
    if not isinstance(cle, str) or not cle:
        raise ValueError("La clé ne doit pas être vide.")

    cle = cle.upper()

    if not all("A" <= lettre <= "Z" for lettre in cle):
        raise ValueError("La clé doit contenir uniquement des lettres A-Z.")

    return cle


def est_lettre_ascii(caractere):
    """Vérifie si le caractère est une lettre ASCII."""
    return caractere.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and caractere.isascii()


def chiffrer_autoclave(message, cle):
    """Chiffre avec un autoclave à texte clair."""
    cle = valider_cle(cle)
    resultat = []
    lettres_claires = []

    for caractere in message:
        if est_lettre_ascii(caractere):
            lettre = caractere.upper()
            position = len(lettres_claires)

            if position < len(cle):
                lettre_cle = cle[position]
            else:
                lettre_cle = lettres_claires[position - len(cle)]

            valeur = (
                ord(lettre) - ord("A")
                + ord(lettre_cle) - ord("A")
            ) % 26

            chiffre = chr(valeur + ord("A"))

            if caractere.islower():
                chiffre = chiffre.lower()

            resultat.append(chiffre)
            lettres_claires.append(lettre)
        else:
            resultat.append(caractere)

    return "".join(resultat)


def dechiffrer_autoclave(message, cle):
    """Déchiffre avec un autoclave à texte clair."""
    cle = valider_cle(cle)
    resultat = []
    lettres_claires = []

    for caractere in message:
        if est_lettre_ascii(caractere):
            lettre = caractere.upper()
            position = len(lettres_claires)

            if position < len(cle):
                lettre_cle = cle[position]
            else:
                lettre_cle = lettres_claires[position - len(cle)]

            valeur = (
                ord(lettre) - ord("A")
                - (ord(lettre_cle) - ord("A"))
            ) % 26

            clair = chr(valeur + ord("A"))

            if caractere.islower():
                clair = clair.lower()

            resultat.append(clair)
            lettres_claires.append(clair.upper())
        else:
            resultat.append(caractere)

    return "".join(resultat)
