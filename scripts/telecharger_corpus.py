
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile
from io import BytesIO
import re
import unicodedata
import xml.etree.ElementTree as ET

URL = (
    "https://codeload.github.com/"
    "COST-ELTeC/ELTeC-fra/zip/refs/heads/master"
)


def nettoyer_texte(texte):
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(
        c for c in texte
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^A-Z]", "", texte.upper())


def extraire_texte_xml(contenu):
    try:
        racine = ET.fromstring(contenu)
        return " ".join(racine.itertext())
    except ET.ParseError:
        texte = contenu.decode("utf-8", errors="replace")
        return re.sub(r"<[^>]+>", " ", texte)


def main():
    print("Téléchargement du corpus ELTeC-fra...")

    requete = Request(
        URL,
        headers={"User-Agent": "Vigenere-Squad/1.0"}
    )

    with urlopen(requete, timeout=120) as reponse:
        archive = BytesIO(reponse.read())

    print("Archive reçue. Extraction des textes...")

    corpus = []
    nombre_textes = 0

    with ZipFile(archive) as zip_file:
        fichiers = [
            nom for nom in zip_file.namelist()
            if "/level1/" in nom.lower()
            and nom.lower().endswith(".xml")
        ]

        for nom in fichiers:
            contenu = zip_file.read(nom)
            texte = extraire_texte_xml(contenu)
            texte = nettoyer_texte(texte)

            if len(texte) >= 1000:
                corpus.append(texte)
                nombre_textes += 1
                print(f"Texte {nombre_textes} : {len(texte)} lettres")

    if not corpus:
        raise RuntimeError(
            "Aucun texte exploitable trouvé dans l'archive."
        )

    contenu_final = "\n".join(corpus)

    dossier = Path("data")
    dossier.mkdir(exist_ok=True)

    chemin = dossier / "corpus_francais.txt"
    chemin.write_text(contenu_final, encoding="utf-8")

    print("\nCorpus français créé avec succès !")
    print("Nombre de textes :", nombre_textes)
    print("Nombre total de lettres :", len(contenu_final))
    print("Fichier :", chemin)


if __name__ == "__main__":
    main()
