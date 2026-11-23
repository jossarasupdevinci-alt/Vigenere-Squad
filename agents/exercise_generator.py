
import random
from dataclasses import dataclass
from typing import Any

from scripts.generer_corpus import charger_source, chiffrer_message

METHODES = (
    "cesar",
    "affine",
    "vigenere",
    "autoclave",
    "substitution",
    "transposition",
)


@dataclass(frozen=True)
class Exercice:
    enonce: dict[str, Any]
    solution: dict[str, Any]


def generer_exercice(
    methode: str | None = None,
    seed: int | None = None,
) -> Exercice:
    rng = random.Random(seed)

    if methode is None:
        methode = rng.choice(METHODES)

    if methode not in METHODES:
        raise ValueError(f"Méthode inconnue : {methode}")

    source = charger_source()
    longueur = rng.randint(80, 200)
    debut = rng.randint(0, len(source) - longueur)
    texte_clair = source[debut:debut + longueur]

    texte_chiffre, cle = chiffrer_message(
        methode,
        texte_clair,
        rng,
    )

    enonce = {
        "methode": methode,
        "texte_chiffre": texte_chiffre,
        "longueur": len(texte_chiffre),
        "consigne": f"Déchiffrez ce message avec la méthode {methode}.",
    }

    solution = {
        "texte_clair": texte_clair,
        "texte_chiffre": texte_chiffre,
        "cle": cle,
        "methode": methode,
    }

    return Exercice(enonce=enonce, solution=solution)
