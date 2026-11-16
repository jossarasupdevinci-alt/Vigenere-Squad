
import argparse
import json
import math
import random
import string
from pathlib import Path

try:
    from .chiffrement_cesar import chiffrer_cesar
    from .chiffrement_affine import chiffrer_affine
    from .chiffrement_vigenere import chiffrer_vigenere
    from .chiffrement_autoclave import chiffrer_autoclave
    from .chiffrement_substitution import chiffrer_substitution
    from .chiffrement_transposition import chiffrer_transposition
except ImportError:
    from chiffrement_cesar import chiffrer_cesar
    from chiffrement_affine import chiffrer_affine
    from chiffrement_vigenere import chiffrer_vigenere
    from chiffrement_autoclave import chiffrer_autoclave
    from chiffrement_substitution import chiffrer_substitution
    from chiffrement_transposition import chiffrer_transposition

RACINE = Path(__file__).resolve().parent.parent
FICHIER_SOURCE = RACINE / "data" / "corpus_francais.txt"
DOSSIER_SORTIE = RACINE / "data" / "corpus_genere"
DOSSIER_MESSAGES = DOSSIER_SORTIE / "messages"
ALPHABET = string.ascii_uppercase


def nettoyer_texte(texte):
    resultat = []
    for caractere in texte.upper():
        if caractere in ALPHABET or caractere.isspace():
            resultat.append(caractere)
    return " ".join("".join(resultat).split())


def generer_cle_lettres(longueur, rng):
    return "".join(rng.choice(ALPHABET) for _ in range(longueur))


def generer_cle_substitution(rng):
    lettres = list(ALPHABET)
    rng.shuffle(lettres)
    return "".join(lettres)


def generer_cle_affine(rng):
    valeurs_a = [
        a for a in range(1, 26)
        if math.gcd(a, 26) == 1
    ]
    return {
        "a": rng.choice(valeurs_a),
        "b": rng.randint(0, 25)
    }


def chiffrer_message(methode, texte, rng):
    if methode == "cesar":
        cle = rng.randint(1, 25)
        return chiffrer_cesar(texte, cle), cle

    if methode == "affine":
        cle = generer_cle_affine(rng)
        chiffre = chiffrer_affine(texte, cle["a"], cle["b"])
        return chiffre, cle

    if methode == "vigenere":
        cle = generer_cle_lettres(rng.randint(3, 12), rng)
        return chiffrer_vigenere(texte, cle), cle

    if methode == "autoclave":
        cle = generer_cle_lettres(rng.randint(3, 12), rng)
        return chiffrer_autoclave(texte, cle), cle

    if methode == "substitution":
        cle = generer_cle_substitution(rng)
        return chiffrer_substitution(texte, cle), cle

    if methode == "transposition":
        cle = generer_cle_lettres(rng.randint(3, 12), rng)
        return chiffrer_transposition(texte, cle), cle

    raise ValueError(f"Méthode inconnue : {methode}")


def charger_source():
    if not FICHIER_SOURCE.exists():
        raise FileNotFoundError(
            f"Corpus source introuvable : {FICHIER_SOURCE}"
        )

    texte = nettoyer_texte(
        FICHIER_SOURCE.read_text(
            encoding="utf-8",
            errors="replace"
        )
    )

    if len(texte) < 200:
        raise ValueError("Le corpus source est trop court.")

    return texte


def generer_corpus(nombre=150, seed=42):
    if nombre < 6:
        raise ValueError("Le nombre de messages doit être au moins 6.")

    rng = random.Random(seed)
    source = charger_source()

    methodes = [
        "cesar",
        "affine",
        "vigenere",
        "autoclave",
        "substitution",
        "transposition",
    ]

    DOSSIER_MESSAGES.mkdir(parents=True, exist_ok=True)

    # Supprime les anciens messages pour éviter les fichiers résiduels.
    for ancien_fichier in DOSSIER_MESSAGES.glob("message_*.txt"):
        ancien_fichier.unlink()

    references = []

    for numero in range(1, nombre + 1):
        methode = methodes[(numero - 1) % len(methodes)]

        longueur = rng.randint(80, 2000)
        debut_max = max(0, len(source) - longueur)
        debut = rng.randint(0, debut_max)

        texte_clair = source[debut:debut + longueur]

        if len(texte_clair) < 80:
            texte_clair = (texte_clair * 2)[:80]

        texte_chiffre, cle = chiffrer_message(
            methode,
            texte_clair,
            rng
        )

        nom = f"message_{numero:03d}.txt"

        (DOSSIER_MESSAGES / nom).write_text(
            texte_chiffre,
            encoding="utf-8"
        )

        references.append({
            "id": numero,
            "fichier": nom,
            "methode": methode,
            "cle": cle,
            "longueur": len(texte_clair),
            "texte_clair": texte_clair,
            "texte_chiffre": texte_chiffre,
        })

    fichier_reference = DOSSIER_SORTIE / "reference_privee.json"

    fichier_reference.write_text(
        json.dumps(references, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    bilan = {}
    for entree in references:
        methode = entree["methode"]
        bilan[methode] = bilan.get(methode, 0) + 1

    print(f"Corpus généré : {len(references)} messages")
    print(f"Seed : {seed}")
    print("Répartition :")

    for methode, total in bilan.items():
        print(f"  {methode} : {total}")

    print(f"Messages accessibles aux agents : {DOSSIER_MESSAGES}")
    print(f"Référence privée : {fichier_reference}")

    return references


def main():
    parser = argparse.ArgumentParser(
        description="Génération d'un corpus de textes chiffrés."
    )

    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--nombre", type=int, default=150)

    args = parser.parse_args()

    generer_corpus(
        nombre=args.nombre,
        seed=args.seed
    )


if __name__ == "__main__":
    main()
