
import pytest

from scripts.chiffrement_cesar import (
    chiffrer_cesar,
    dechiffrer_cesar
)


def test_chiffrement_cesar():
    assert chiffrer_cesar("BONJOUR", 3) == "ERQMRXU"


def test_dechiffrement_cesar():
    assert dechiffrer_cesar("ERQMRXU", 3) == "BONJOUR"


def test_decalage_circulaire():
    assert chiffrer_cesar("XYZ", 3) == "ABC"


def test_conservation_espaces_et_ponctuation():
    assert chiffrer_cesar("BONJOUR, MONDE !", 3) == "ERQMRXU, PRQGH !"


def test_chiffrement_reversible():
    message = "BONJOUR, MONDE !"
    chiffre = chiffrer_cesar(message, 3)
    assert dechiffrer_cesar(chiffre, 3) == message
