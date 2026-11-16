
import pytest

from scripts.chiffrement_substitution import (
    chiffrer_substitution,
    dechiffrer_substitution,
    valider_cle
)

CLE = "QWERTYUIOPASDFGHJKLZXCVBNM"


def test_chiffrement_substitution():
    assert chiffrer_substitution("BONJOUR", CLE) == "WGFPGXK"


def test_dechiffrement_substitution():
    assert dechiffrer_substitution("WGFPGXK", CLE) == "BONJOUR"


def test_chiffrement_reversible():
    message = "BONJOUR"
    chiffre = chiffrer_substitution(message, CLE)
    assert dechiffrer_substitution(chiffre, CLE) == message


def test_cle_trop_courte():
    with pytest.raises(ValueError):
        valider_cle("ABCDE")


def test_cle_avec_doublons():
    with pytest.raises(ValueError):
        valider_cle("A" * 26)


def test_conservation_ponctuation():
    assert chiffrer_substitution("BONJOUR !", CLE) == "WGFPGXK !"


def test_cle_invalide():
    with pytest.raises(ValueError):
        valider_cle("12345678901234567890123456")

