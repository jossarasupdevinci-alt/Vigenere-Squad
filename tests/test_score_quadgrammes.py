import pytest

from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score,
    calculer_score_moyen,
)


def test_calculer_score_quadgramme_connu():
    modele = {"BONJ": -2.0, "ONJO": -3.0, "NJOU": -1.0}
    assert calculer_score("BONJOU", modele) == -6.0


def test_calculer_score_quadgramme_inconnu():
    modele = {"ABCD": -2.0}
    assert calculer_score("WXYZ", modele) == -10.0


def test_calculer_score_message_trop_court():
    assert calculer_score("ABC", {}) == float("-inf")


def test_calculer_score_moyen():
    modele = {"BONJ": -2.0, "ONJO": -3.0, "NJOU": -1.0}
    assert calculer_score_moyen("BONJOU", modele) == -2.0


def test_calculer_score_moyen_message_trop_court():
    assert calculer_score_moyen("ABC", {}) == float("-inf")


def test_charger_modele_fichier_vide(tmp_path):
    fichier = tmp_path / "modele.txt"
    fichier.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="vide"):
        charger_modele(fichier)