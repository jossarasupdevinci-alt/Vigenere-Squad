
import argparse
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NOMBRE_QUADGRAMMES = 26 ** 4


def nettoyer_texte(texte):
    # Supprimer les accents
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(
        caractere for caractere in texte
        if unicodedata.category(caractere) != "Mn"
    )

    # Conserver uniquement les lettres A-Z
    return "".join(re.findall(r"[A-Z]", texte.upper()))


def entrainer_modele(texte, alpha=0.1):
    texte = nettoyer_texte(texte)

    if len(texte) < 4:
        raise ValueError("Le corpus doit contenir au moins 4 lettres.")

    compteurs = Counter(
        texte[i:i + 4]
        for i in range(len(texte) - 3)
    )

    total = sum(compteurs.values())
    denominateur = total + alpha * NOMBRE_QUADGRAMMES

    probabilites = {}

    for quadgramme, nombre in compteurs.items():
        probabilite = (nombre + alpha) / denominateur
        probabilites[quadgramme] = math.log10(probabilite)

    return probabilites


def sauvegarder_modele(probabilites, chemin):
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)

    with chemin.open("w", encoding="utf-8") as fichier:
        for quadgramme, score in sorted(probabilites.items()):
            fichier.write(f"{quadgramme} {score}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Entraine un modele statistique de quadgrammes."
    )
    parser.add_argument("--input", required=True, help="Fichier du corpus français")
    parser.add_argument(
        "--output",
        default="data/quadgrammes_fr.txt",
        help="Fichier de sortie du modèle"
    )

    args = parser.parse_args()

    chemin_corpus = Path(args.input)

    if not chemin_corpus.exists():
        raise FileNotFoundError(f"Corpus introuvable : {chemin_corpus}")

    texte = chemin_corpus.read_text(encoding="utf-8")
    probabilites = entrainer_modele(texte)

    sauvegarder_modele(probabilites, args.output)

    print("Entrainement termine.")
    print("Quadgrammes appris :", len(probabilites))
    print("Modele sauvegarde :", args.output)


if __name__ == "__main__":
    main()
