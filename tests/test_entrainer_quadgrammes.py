
import math
import pytest

from scripts.entrainer_quadgrammes import (
    nettoyer_texte,
    entrainer_modele,
    sauvegarder_modele,
    main,
)


def test_nettoyer_texte_accents():
    assert nettoyer_texte("Éléphant à Noël") == "ELEPHANTANOEL"


def test_nettoyer_texte_caracteres_speciaux():
    assert nettoyer_texte("Bonjour ! 123") == "BONJOUR"


def test_nettoyer_texte_vide():
    assert nettoyer_texte("") == ""


def test_entrainer_modele():
    modele = entrainer_modele("BONJOUR BONJOUR")

    assert "BONJ" in modele
    assert isinstance(modele["BONJ"], float)


def test_entrainer_modele_trop_court():
    with pytest.raises(ValueError):
        entrainer_modele("ABC")


def test_entrainer_modele_probabilites():
    modele = entrainer_modele("BONJOUR")

    assert all(score < 0 for score in modele.values())


def test_entrainer_modele_alpha_personnalise():
    modele = entrainer_modele("BONJOUR BONJOUR", alpha=0.5)

    assert len(modele) > 0


def test_sauvegarder_modele(tmp_path):
    modele = {"BONJ": -1.5, "ONJO": -2.0}
    fichier = tmp_path / "resultats" / "modele.txt"

    sauvegarder_modele(modele, fichier)

    assert fichier.exists()
    contenu = fichier.read_text(encoding="utf-8")
    assert "BONJ -1.5" in contenu


def test_sauvegarder_modele_trie(tmp_path):
    modele = {"ZZZZ": -3.0, "AAAA": -1.0}
    fichier = tmp_path / "modele.txt"

    sauvegarder_modele(modele, fichier)

    lignes = fichier.read_text(encoding="utf-8").splitlines()
    assert lignes[0].startswith("AAAA")


def test_main_entrainement(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus.txt"
    sortie = tmp_path / "modele.txt"

    corpus.write_text("BONJOUR TOUT LE MONDE", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["entrainer_quadgrammes.py", "--input", str(corpus),
         "--output", str(sortie)]
    )

    main()

    assert sortie.exists()


def test_main_corpus_absent(tmp_path, monkeypatch):
    corpus = tmp_path / "absent.txt"

    monkeypatch.setattr(
        "sys.argv",
        ["entrainer_quadgrammes.py", "--input", str(corpus)]
    )

    with pytest.raises(FileNotFoundError):
        main()
