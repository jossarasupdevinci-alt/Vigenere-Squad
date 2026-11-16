
from io import BytesIO
from zipfile import ZipFile

import pytest

from scripts import telecharger_corpus as tc


def test_nettoyer_texte():
    assert tc.nettoyer_texte("Éléphant à Noël 123!") == "ELEPHANTANOEL"


def test_extraire_texte_xml_valide():
    xml = b"<root><p>Bonjour le monde</p></root>"

    resultat = tc.extraire_texte_xml(xml)

    assert "Bonjour le monde" in resultat


def test_extraire_xml_invalide():
    xml = b"<root><p>Bonjour le monde"

    resultat = tc.extraire_texte_xml(xml)

    assert "Bonjour le monde" in resultat


def creer_archive_test():
    archive = BytesIO()

    with ZipFile(archive, "w") as zip_file:
        texte = "BONJOUR TOUT LE MONDE " * 100
        xml = f"<root><p>{texte}</p></root>"

        zip_file.writestr(
            "ELTeC-fra-master/level1/test.xml",
            xml
        )

        zip_file.writestr(
            "ELTeC-fra-master/autre/test.xml",
            xml
        )

    archive.seek(0)
    return archive.getvalue()


def test_main_telechargement_reussi(tmp_path, monkeypatch):
    archive = creer_archive_test()

    class FausseReponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return archive

    monkeypatch.setattr(
        tc,
        "urlopen",
        lambda *args, **kwargs: FausseReponse()
    )

    monkeypatch.chdir(tmp_path)

    tc.main()

    fichier = tmp_path / "data" / "corpus_francais.txt"

    assert fichier.exists()
    assert len(fichier.read_text(encoding="utf-8")) >= 1000


def test_main_aucun_texte_exploitable(tmp_path, monkeypatch):
    archive = BytesIO()

    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr(
            "ELTeC-fra-master/level1/court.xml",
            "<root>Bonjour</root>"
        )

    contenu = archive.getvalue()

    class FausseReponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def read(self):
            return contenu

    monkeypatch.setattr(
        tc,
        "urlopen",
        lambda *args, **kwargs: FausseReponse()
    )

    monkeypatch.chdir(tmp_path)

    with pytest.raises(RuntimeError):
        tc.main()


def test_main_erreur_telechargement(monkeypatch):
    def erreur(*args, **kwargs):
        raise OSError("Erreur réseau simulée")

    monkeypatch.setattr(tc, "urlopen", erreur)

    with pytest.raises(OSError):
        tc.main()
