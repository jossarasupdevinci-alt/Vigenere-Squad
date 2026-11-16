
import json
from pathlib import Path

from scripts.generer_corpus import generer_corpus


def test_nombre_de_messages(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    monkeypatch.setattr(generateur, "DOSSIER_SORTIE", tmp_path)
    monkeypatch.setattr(
        generateur, "DOSSIER_MESSAGES", tmp_path / "messages"
    )

    generateur.generer_corpus(nombre=12, seed=42)

    fichiers = list((tmp_path / "messages").glob("message_*.txt"))
    assert len(fichiers) == 12


def test_repartition_des_methodes(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    monkeypatch.setattr(generateur, "DOSSIER_SORTIE", tmp_path)
    monkeypatch.setattr(
        generateur, "DOSSIER_MESSAGES", tmp_path / "messages"
    )

    generateur.generer_corpus(nombre=12, seed=42)

    references = json.loads(
        (tmp_path / "reference_privee.json").read_text(encoding="utf-8")
    )

    methodes = {}
    for entree in references:
        methodes[entree["methode"]] = (
            methodes.get(entree["methode"], 0) + 1
        )

    assert len(methodes) == 6
    assert all(nombre == 2 for nombre in methodes.values())


def test_longueurs_valides(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    monkeypatch.setattr(generateur, "DOSSIER_SORTIE", tmp_path)
    monkeypatch.setattr(
        generateur, "DOSSIER_MESSAGES", tmp_path / "messages"
    )

    generateur.generer_corpus(nombre=12, seed=42)

    references = json.loads(
        (tmp_path / "reference_privee.json").read_text(encoding="utf-8")
    )

    assert all(80 <= entree["longueur"] <= 2000 for entree in references)


def test_reference_privee_presente(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    monkeypatch.setattr(generateur, "DOSSIER_SORTIE", tmp_path)
    monkeypatch.setattr(
        generateur, "DOSSIER_MESSAGES", tmp_path / "messages"
    )

    generateur.generer_corpus(nombre=12, seed=42)

    fichier = tmp_path / "reference_privee.json"
    assert fichier.exists()

    references = json.loads(fichier.read_text(encoding="utf-8"))
    assert len(references) == 12
    assert all("cle" in entree for entree in references)


def test_reproductibilite(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    dossier_messages = tmp_path / "messages"
    monkeypatch.setattr(generateur, "DOSSIER_SORTIE", tmp_path)
    monkeypatch.setattr(generateur, "DOSSIER_MESSAGES", dossier_messages)

    generateur.generer_corpus(nombre=12, seed=42)

    premiere_generation = {
        fichier.name: fichier.read_bytes()
        for fichier in dossier_messages.glob("message_*.txt")
    }

    generateur.generer_corpus(nombre=12, seed=42)

    seconde_generation = {
        fichier.name: fichier.read_bytes()
        for fichier in dossier_messages.glob("message_*.txt")
    }

    assert premiere_generation == seconde_generation


def test_corpus_source_introuvable(tmp_path, monkeypatch):
    import scripts.generer_corpus as generateur

    monkeypatch.setattr(
        generateur, "FICHIER_SOURCE", tmp_path / "inexistant.txt"
    )

    try:
        generateur.charger_source()
        assert False, "Une erreur était attendue."
    except FileNotFoundError:
        pass
