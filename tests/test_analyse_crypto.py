
import pytest

from scripts.analyse_frequentielle import analyser_frequences
from scripts.indice_coincidence import calculer_indice_coincidence
from scripts.kasiski import analyser_kasiski
from scripts.force_brute_cesar import force_brute_cesar
from scripts.analyse_linguistique import analyser_langue
from scripts.attaque_cesar_khi_deux import classer_resultats


def test_analyse_frequentielle():
    resultats = analyser_frequences("BONJOUR BONJOUR")
    assert resultats["O"] == 28.57
    assert resultats["B"] == 14.29


def test_frequences_message_vide():
    with pytest.raises(ValueError):
        analyser_frequences("123 !")


def test_indice_coincidence():
    resultat = calculer_indice_coincidence("BONJOUR BONJOUR")
    assert round(resultat, 4) == 0.1209


def test_indice_coincidence_message_trop_court():
    with pytest.raises(ValueError):
        calculer_indice_coincidence("A")


def test_analyse_kasiski():
    _, _, pgcd = analyser_kasiski("ABCXYZABCXYZABCXYZ")
    assert pgcd == 6


def test_force_brute_cesar():
    resultats = force_brute_cesar("ERQMRXU")
    assert resultats[3] == "BONJOUR"


def test_analyse_linguistique():
    assert analyser_langue("BONJOUR") == 1.0


def test_classement_cesar():
    resultats = classer_resultats("ERQMRXU")
    meilleure_proposition = resultats[0]

    assert meilleure_proposition[1] == 3
    assert meilleure_proposition[2] == "BONJOUR"


def test_analyse_linguistique_plusieurs_mots():
    assert analyser_langue("BONJOUR MONDE") == 1.0


def test_analyse_linguistique_texte_inconnu():
    assert analyser_langue("XYZZY QWERTY") == 0.0


def test_analyse_linguistique_message_vide():
    assert analyser_langue("") == 0.0



def test_force_brute_contient_26_cles():
    resultats = force_brute_cesar("ERQMRXU")
    assert len(resultats) == 26


def test_force_brute_cle_zero():
    resultats = force_brute_cesar("BONJOUR")
    assert resultats[0] == "BONJOUR"


def test_force_brute_conserve_ponctuation():
    resultats = force_brute_cesar("ERQMRXU !")
    assert resultats[3] == "BONJOUR !"


from pathlib import Path
import pytest

from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score,
    calculer_score_moyen,
)


def test_charger_modele_valide(tmp_path):
    fichier = tmp_path / "modele.txt"
    fichier.write_text(
        "BONJ -1.5\nONJO -2.0\nJOUR -1.2\n",
        encoding="utf-8"
    )

    modele = charger_modele(fichier)

    assert modele["BONJ"] == -1.5
    assert len(modele) == 3


def test_charger_modele_ligne_invalide(tmp_path):
    fichier = tmp_path / "modele.txt"
    fichier.write_text(
        "BONJ -1.5\nLIGNE_INVALIDE\nONJO -2.0\n",
        encoding="utf-8"
    )

    modele = charger_modele(fichier)

    assert len(modele) == 2


def test_charger_modele_vide(tmp_path):
    fichier = tmp_path / "modele.txt"
    fichier.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        charger_modele(fichier)


def test_charger_modele_fichier_absent(tmp_path):
    fichier = tmp_path / "inexistant.txt"

    with pytest.raises(FileNotFoundError):
        charger_modele(fichier)


def test_calculer_score_quadgrammes():
    modele = {"BONJ": -1.0, "ONJO": -2.0, "NJOU": -3.0, "JOUR": -4.0}

    assert calculer_score("BONJOUR", modele) == -10.0


def test_score_message_trop_court():
    modele = {"BONJ": -1.0}

    assert calculer_score("ABC", modele) == float("-inf")


def test_score_message_sans_lettres():
    modele = {"BONJ": -1.0}

    assert calculer_score("123 !?", modele) == float("-inf")


def test_score_quadgramme_inconnu():
    modele = {"BONJ": -1.0}

    assert calculer_score("ZZZZ", modele) == -10.0


def test_calculer_score_moyen():
    modele = {"BONJ": -1.0, "ONJO": -2.0, "NJOU": -3.0, "JOUR": -4.0}

    assert calculer_score_moyen("BONJOUR", modele) == -2.5


def test_score_moyen_message_court():
    modele = {"BONJ": -1.0}

    assert calculer_score_moyen("ABC", modele) == float("-inf")
