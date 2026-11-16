
from scripts.attaque_substitution import (
    generer_cle_aleatoire,
    modifier_cle,
    chiffrer_substitution,
    dechiffrer_substitution,
    evaluer_cle,
    recuit_simule,
    ALPHABET,
)

CLE = "QWERTYUIOPASDFGHJKLZXCVBNM"


def test_generation_cle():
    cle = generer_cle_aleatoire()
    assert len(cle) == 26
    assert set(cle) == set(ALPHABET)


def test_modification_cle():
    nouvelle_cle = modifier_cle(CLE)
    assert len(nouvelle_cle) == 26
    assert set(nouvelle_cle) == set(ALPHABET)
    assert nouvelle_cle != CLE


def test_chiffrement_dechiffrement():
    texte = "BONJOUR TOUT LE MONDE"
    chiffre = chiffrer_substitution(texte, CLE)
    dechiffre = dechiffrer_substitution(chiffre, CLE)
    assert dechiffre == texte


def test_conservation_ponctuation():
    texte = "BONJOUR !"
    chiffre = chiffrer_substitution(texte, CLE)
    assert chiffre.endswith(" !")


def test_evaluer_cle():
    modele = {"BONJ": -1.0, "ONJO": -1.0, "NJOU": -1.0, "JOUR": -1.0}
    score = evaluer_cle("WGFPGXK", CLE, modele)
    assert isinstance(score, float)


def test_recuit_simule_reproductible():
    modele = {
        "BONJ": -1.0,
        "ONJO": -1.0,
        "NJOU": -1.0,
        "JOUR": -1.0,
    }
    message = "WGFPGXK"

    resultat1 = recuit_simule(
        message, modele, iterations=100, graine=42
    )
    resultat2 = recuit_simule(
        message, modele, iterations=100, graine=42
    )

    assert resultat1 == resultat2


from scripts.attaque_substitution import charger_texte_test


def test_charger_texte_test():
    texte = charger_texte_test()

    assert len(texte) == 1000
    assert texte.isalpha()
    assert texte.isupper()


def test_recuit_simule_retourne_une_cle_valide():
    modele = {"BONJ": -1.0, "ONJO": -2.0, "NJOU": -3.0, "JOUR": -4.0}

    cle, texte, score = recuit_simule(
        "WGFPGXK",
        modele,
        iterations=100,
        graine=42
    )

    assert len(cle) == 26
    assert len(set(cle)) == 26
    assert isinstance(texte, str)
    assert isinstance(score, float)
