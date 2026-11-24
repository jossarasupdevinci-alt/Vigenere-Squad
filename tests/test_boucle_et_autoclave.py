import importlib
import agents.cryptanalyst_agent as ca_mod
from scripts.chiffrement_autoclave import chiffrer_autoclave
from scripts.attaque_autoclave import (
    estimer_longueur_cle_autoclave,
    attaquer_autoclave,
)
from scripts.kasiski import analyser_kasiski
from scripts.score_quadgrammes import charger_modele
from agents.orchestrator import Orchestrator
from agents.state import AgentResult


TEXTE_LONG = (
    "LA CRYPTOGRAPHIE MODERNE REPOSE SUR DES PRINCIPES MATHEMATIQUES "
    "RIGOUREUX MAIS LES CHIFFREMENTS HISTORIQUES COMME VIGENERE OU "
    "AUTOCLAVE PERMETTENT DE COMPRENDRE LES BASES DE LA CRYPTANALYSE "
    "STATISTIQUE ET LIMPORTANCE DE LA LONGUEUR DES TEXTES CHIFFRES"
)


def test_autoclave_kasiski_echoue_mais_attaque_reussit():
    """
    Exigence 5.2 : montre que Kasiski ne retrouve pas la longueur de clé
    sur un autoclave, alors que l'attaque dédiée retrouve la clé et le clair.
    """
    cle_secrete = "SECRET"
    chiffre = chiffrer_autoclave(TEXTE_LONG, cle_secrete)

    res_kasiski = analyser_kasiski(chiffre)
    longueur_kasiski = res_kasiski[2] if isinstance(res_kasiski, tuple) else None
    assert longueur_kasiski != len(cle_secrete)

    estimations = estimer_longueur_cle_autoclave(chiffre, max_len=10)
    meilleures_longueurs = [longueur for longueur, _ in estimations[:2]]
    assert len(cle_secrete) in meilleures_longueurs

    modele = charger_modele()
    resultat = attaquer_autoclave(chiffre, modele, max_len=10)
    assert resultat["cle"] == cle_secrete
    assert resultat["texte_clair"] == TEXTE_LONG


def test_orchestrator_boucle_de_correction(tmp_path):
    """
    Vérifie que si le LinguistAgent rejette le premier essai,
    l'Orchestrator relance une itération avec exclusion du procédé rejeté.
    """
    importlib.reload(ca_mod)
    orchestrator = Orchestrator(max_iterations=3)
    orchestrator.logger.log_path = tmp_path / "traces_boucle.jsonl"

    seuils = [-0.1, -4.5, -4.5]
    appel = {"n": 0}
    analyse_originale = orchestrator.linguist.analyze

    def analyse_simulee(state):
        orchestrator.linguist.quadgram_threshold = seuils[min(appel["n"], 2)]
        appel["n"] += 1
        return analyse_originale(state)

    orchestrator.linguist.analyze = analyse_simulee

    chiffre = chiffrer_autoclave(TEXTE_LONG, "SECRET")
    state = orchestrator.run(chiffre)

    assert state.iteration_count >= 2
    assert "autoclave" in state.excluded_ciphers
    assert len(state.excluded_ciphers) >= 2


def test_orchestrator_robustesse_defaillance(tmp_path):
    """
    Exigence 6.3 : vérifie que l'orchestrateur réessaie et s'arrête proprement
    en cas d'échec répété d'un agent (exception ou réponse vide).
    """
    orchestrator = Orchestrator(max_iterations=2, max_retries=2)
    orchestrator.logger.log_path = tmp_path / "traces_panne.jsonl"

    def agent_en_panne(state):
        raise RuntimeError("Délai dépassé / JSON invalide")

    orchestrator.cryptanalyst.analyze = agent_en_panne
    state = orchestrator.run("ERQMRXU WRXW OH PRQGH")

    assert any("CryptanalystAgent" in err for err in state.errors)
    assert state.is_plausible is False
