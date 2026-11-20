import runpy
from pathlib import Path
import re

# Petit vocabulaire franÃ§ais de dÃ©part
MOTS_FRANCAIS = {
    "BONJOUR", "SALUT", "MERCI", "MAISON", "MONDE",
    "ECOLE", "CHAT", "CHIEN", "ORDINATEUR", "SECURITE",
    "LE", "LA", "LES", "UN", "UNE", "DES",
    "ET", "EST", "DANS", "POUR", "AVEC",
    "JE", "TU", "IL", "ELLE", "NOUS", "VOUS",
    "MON", "TON", "SON", "QUI", "QUE",
    "MESSAGE", "TEXTE", "FRANCAIS"
}


def analyser_langue(message):
    mots = re.findall(r"[A-Z]+", message.upper())

    if not mots:
        return 0.0

    mots_reconnus = sum(
        1 for mot in mots if mot in MOTS_FRANCAIS
    )

    return mots_reconnus / len(mots)

if __name__ == "__main__":
    message = "BONJOUR"

    score = analyser_langue(message)

    print("Message analyse :", message)
    print("Score linguistique :", round(score, 2))
    print("Mots reconnus :", score > 0)
