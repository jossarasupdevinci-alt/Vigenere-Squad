
import pytest

from scripts.chiffrement_affine import (
    chiffrer_affine,
    dechiffrer_affine,
    valider_cle
)


def test_chiffrement_affine():
    assert chiffrer_affine("BONJOUR", 5, 8) == "NAVBAEP"


def test_dechiffrement_affine():
    assert dechiffrer_affine("NAVBAEP", 5, 8) == "BONJOUR"


def test_chiffrement_reversible():
    message = "BONJOUR"
    chiffre = chiffrer_affine(message, 5, 8)
    assert dechiffrer_affine(chiffre, 5, 8) == message


def test_cle_a_invalide():
    with pytest.raises(ValueError):
        valider_cle(2, 8)


def test_cle_non_entiere():
    with pytest.raises(ValueError):
        valider_cle(3.5, 8)


def test_conservation_ponctuation():
    assert chiffrer_affine("BONJOUR !", 5, 8) == "NAVBAEP !"
