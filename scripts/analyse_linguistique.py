import runpy
from pathlib import Path
import re

# Petit vocabulaire français de départ
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
    
def test_analyse_linguistique_execution_directe(capsys):
    chemin = Path(__file__).resolve().parents[1]
    script = chemin / "scripts" / "analyse_linguistique.py"

    runpy.run_path(str(script), run_name="__main__")

    sortie = capsys.readouterr().out

    assert "Message analyse : BONJOUR" in sortie
    assert "Score linguistique : 1.0" in sortie
    assert "Mots reconnus : True" in sortie