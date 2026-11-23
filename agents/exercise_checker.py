
import re
from typing import Any

from scripts.chiffrement_cesar import dechiffrer_cesar
from scripts.chiffrement_affine import dechiffrer_affine
from scripts.chiffrement_vigenere import dechiffrer_vigenere
from scripts.chiffrement_autoclave import dechiffrer_autoclave
from scripts.chiffrement_substitution import dechiffrer_substitution
from scripts.chiffrement_transposition import dechiffrer_transposition


def normaliser_reponse(texte: str) -> str:
    """Normalise les espaces et la casse."""
    if not isinstance(texte, str):
        raise TypeError("La réponse doit être une chaîne de caractères.")

    return re.sub(r"\s+", " ", texte.strip()).upper()


def verifier_reponse(
    texte_propose: str,
    solution: dict[str, Any],
) -> dict[str, Any]:
    """Vérifie une réponse sans révéler la clé."""

    if not isinstance(solution, dict):
        raise TypeError("La solution doit être un dictionnaire.")

    methode = solution.get("methode")
    texte_chiffre = solution.get("texte_chiffre")
    cle = solution.get("cle")

    if not isinstance(texte_chiffre, str) or cle is None:
        raise ValueError("La solution est incomplète.")

    fonctions = {
        "cesar": lambda: dechiffrer_cesar(texte_chiffre, cle),
        "affine": lambda: dechiffrer_affine(
            texte_chiffre, cle["a"], cle["b"]
        ),
        "vigenere": lambda: dechiffrer_vigenere(texte_chiffre, cle),
        "autoclave": lambda: dechiffrer_autoclave(texte_chiffre, cle),
        "substitution": lambda: dechiffrer_substitution(
            texte_chiffre, cle
        ),
        "transposition": lambda: dechiffrer_transposition(
            texte_chiffre, cle
        ),
    }

    if methode not in fonctions:
        raise ValueError(f"Méthode inconnue : {methode}")

    texte_attendu = fonctions[methode]()

    correcte = (
        normaliser_reponse(texte_propose)
        == normaliser_reponse(texte_attendu)
    )

    return {
        "correcte": correcte,
        "message": (
            "Bonne réponse !"
            if correcte
            else "Réponse incorrecte. Essayez encore."
        ),
    }
