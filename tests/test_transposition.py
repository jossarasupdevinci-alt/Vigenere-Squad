
import pytest

from scripts.chiffrement_transposition import (
    valider_cle,
    chiffrer_transposition,
    dechiffrer_transposition,
)


def test_chiffrement_et_dechiffrement():
    message = "BONJOURTOUTLEMONDE"
    cle = "CHAT"

    chiffre = chiffrer_transposition(message, cle)
    dechiffre = dechiffrer_transposition(chiffre, cle)

    assert dechiffre == message


def test_conservation_espaces_et_ponctuation():
    message = "Bonjour, comment allez-vous ?"
    cle = "SECRET"

    chiffre = chiffrer_transposition(message, cle)
    dechiffre = dechiffrer_transposition(chiffre, cle)

    assert dechiffre == message


def test_cle_vide():
    with pytest.raises(ValueError):
        valider_cle("")


def test_cle_invalide():
    with pytest.raises(ValueError):
        valider_cle("CLE123")


def test_cle_avec_lettres_repetees():
    assert valider_cle("ANANAS") == "ANANAS"


def test_cle_en_minuscules():
    assert valider_cle("chat") == "CHAT"


def test_message_vide():
    assert chiffrer_transposition("", "CHAT") == ""
    assert dechiffrer_transposition("", "CHAT") == ""


def test_message_plus_court_que_la_cle():
    message = "ABC"
    cle = "SECRET"

    chiffre = chiffrer_transposition(message, cle)

    assert dechiffrer_transposition(chiffre, cle) == message


def test_message_avec_accents():
    message = "Été à Paris !"
    cle = "CHAT"

    chiffre = chiffrer_transposition(message, cle)
    dechiffre = dechiffrer_transposition(chiffre, cle)

    assert dechiffre == message
