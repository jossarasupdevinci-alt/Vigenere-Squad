
import pytest

from scripts.chiffrement_vigenere import (
    chiffrer_vigenere,
    dechiffrer_vigenere,
    valider_cle
)


def test_chiffrement_vigenere():
    assert chiffrer_vigenere("BONJOUR", "CLE") == "DZRLZYT"


def test_dechiffrement_vigenere():
    assert dechiffrer_vigenere("DZRLZYT", "CLE") == "BONJOUR"


def test_cle_vide():
    with pytest.raises(ValueError):
        valider_cle("")


def test_cle_invalide():
    with pytest.raises(ValueError):
        valider_cle("CLE123")


def test_chiffrement_reversible():
    message = "BONJOUR"
    cle = "CLE"

    chiffre = chiffrer_vigenere(message, cle)

    assert dechiffrer_vigenere(chiffre, cle) == message
