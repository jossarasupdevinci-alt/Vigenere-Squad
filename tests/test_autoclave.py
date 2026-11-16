
import pytest

from scripts.chiffrement_autoclave import (
    chiffrer_autoclave,
    dechiffrer_autoclave,
    valider_cle,
)


def test_chiffrement_et_dechiffrement():
    message = "BONJOUR TOUT LE MONDE"
    cle = "CLE"

    chiffre = chiffrer_autoclave(message, cle)
    dechiffre = dechiffrer_autoclave(chiffre, cle)

    assert dechiffre == message


def test_conservation_ponctuation():
    message = "Bonjour, comment allez-vous ?"
    cle = "SECRET"

    chiffre = chiffrer_autoclave(message, cle)
    dechiffre = dechiffrer_autoclave(chiffre, cle)

    assert dechiffre == message


def test_cle_vide():
    with pytest.raises(ValueError):
        valider_cle("")


def test_cle_invalide():
    with pytest.raises(ValueError):
        valider_cle("ABC123")


def test_cle_en_minuscules():
    assert valider_cle("cle") == "CLE"


def test_message_vide():
    assert chiffrer_autoclave("", "CLE") == ""


def test_message_plus_court_que_la_cle():
    message = "ABC"
    cle = "SECRET"

    chiffre = chiffrer_autoclave(message, cle)

    assert dechiffrer_autoclave(chiffre, cle) == message


def test_message_avec_accents():
    message = "Été à Paris !"
    cle = "CLE"

    chiffre = chiffrer_autoclave(message, cle)
    dechiffre = dechiffrer_autoclave(chiffre, cle)

    assert dechiffre == message
