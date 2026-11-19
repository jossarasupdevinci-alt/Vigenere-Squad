
import json
from agents.pedagogue_agent import PedagogueAgent
from agents.orchestrator import Orchestrator
from agents.linguist_agent import LinguistAgent
from agents.classifier_agent import ClassifierAgent
from agents.state import SharedState

def test_orchestrator_execute_quatre_agents(tmp_path):
    orchestrator = Orchestrator()
    orchestrator.logger.log_path = tmp_path / "traces.jsonl"

    state = orchestrator.run(
        "ERQMRXU WRXW OH PRQGH"
    )

    noms = [result.agent_name for result in state.results]

    assert "ClassifierAgent" in noms
    assert "CryptanalystAgent" in noms
    assert "LinguistAgent" in noms
    assert "PedagogueAgent" in noms

    assert state.errors == []


def test_orchestrator_retrouve_texte_cesar(tmp_path):
    orchestrator = Orchestrator()
    orchestrator.logger.log_path = tmp_path / "traces.jsonl"

    state = orchestrator.run(
        "ERQMRXU WRXW OH PRQGH"
    )

    assert state.plaintext == "BONJOUR TOUT LE MONDE"
    assert state.candidate_key == "3"
    assert state.cipher_type == "cesar"


def test_orchestrator_enregistre_trace_jsonl(tmp_path):
    orchestrator = Orchestrator()
    log_path = tmp_path / "traces.jsonl"
    orchestrator.logger.log_path = log_path

    orchestrator.run("ERQMRXU WRXW OH PRQGH")

    assert log_path.exists()

    contenu = log_path.read_text(encoding="utf-8")
    entree = json.loads(contenu.strip())

    assert entree["ciphertext"] == "ERQMRXU WRXW OH PRQGH"
    assert len(entree["results"]) == 4


def test_orchestrator_gere_erreur_agent(tmp_path):
    orchestrator = Orchestrator()
    orchestrator.logger.log_path = tmp_path / "traces.jsonl"

    def provoquer_erreur(state):
        raise RuntimeError("Erreur de test")

    orchestrator.classifier.analyze = provoquer_erreur

    state = orchestrator.run(
        "ERQMRXU WRXW OH PRQGH"
    )

    assert any("ClassifierAgent" in erreur for erreur in state.errors)

    resultat = next(
        result for result in state.results
        if result.agent_name == "ClassifierAgent"
    )

    assert resultat.status == "error"
    assert resultat.message == "Erreur de test"


from agents.classifier_agent import ClassifierAgent
from agents.state import SharedState


def test_classifier_texte_trop_court():
    agent = ClassifierAgent()
    state = SharedState(ciphertext="ABC")

    result = agent.analyze(state)

    assert result.status == "error"
    assert result.data["length"] == 3
    assert result in state.results


def test_classifier_ic_eleve():
    agent = ClassifierAgent()
    state = SharedState(ciphertext="AAAAAAAAAAB")

    result = agent.analyze(state)

    assert result.status == "success"
    assert result.data["candidate_ciphers"] == [
        "cesar", "affine", "substitution"
    ]


def test_classifier_ic_intermediaire():
    agent = ClassifierAgent()
    texte = "A" * 8 + "B" * 5 + "C" * 3 + "D" * 2 + "EFGHIJKLMNOPQRSTUVWXYZ"
    state = SharedState(ciphertext=texte)

    result = agent.analyze(state)

    assert result.status == "success"
    assert len(result.data["candidate_ciphers"]) == 6
    assert result.data["candidate_ciphers"] == [
        "cesar", "affine", "vigenere",
        "autoclave", "substitution", "transposition"
    ]

from agents.cryptanalyst_agent import CryptanalystAgent


def test_cryptanalyst_texte_trop_court():
    agent = CryptanalystAgent()
    state = SharedState(ciphertext="ABC")

    result = agent.analyze(state)

    assert result.status == "error"
    assert result.data["text_length"] == 3
    assert result in state.results


def test_cryptanalyst_gere_erreur():
    agent = CryptanalystAgent()
    state = SharedState(ciphertext="BONJOURTOUTLEMONDE")

    def provoquer_erreur(texte):
        raise RuntimeError("Erreur de test")

    import agents.cryptanalyst_agent as module
    module.calculer_indice_coincidence = provoquer_erreur

    result = agent.analyze(state)

    assert result.status == "error"
    assert "Erreur de test" in result.message
    assert result in state.results

def test_cryptanalyst_substitution_retenue(monkeypatch):
    import agents.cryptanalyst_agent as module

    monkeypatch.setattr(
        module,
        "calculer_indice_coincidence",
        lambda texte: 0.05
    )
    monkeypatch.setattr(
        module,
        "analyser_kasiski",
        lambda texte: {}
    )
    monkeypatch.setattr(
        module,
        "force_brute_cesar",
        lambda texte: {}
    )
    monkeypatch.setattr(
        module,
        "dechiffrer_affine",
        lambda texte, a, b: "X" * len(texte)
    )
    monkeypatch.setattr(
        module,
        "calculer_score_moyen",
        lambda texte, modele: -10
    )
    monkeypatch.setattr(
        module,
        "recuit_simule",
        lambda *args, **kwargs: (
            "CLE", "BONJOUR" * 100, 10
        )
    )

    agent = CryptanalystAgent()
    state = SharedState(ciphertext="A" * 500)

    result = agent.analyze(state)

    assert result.status == "success"
    assert state.cipher_type == "substitution"
    assert state.candidate_key == "CLE"
    assert state.plaintext == "BONJOUR" * 100

def test_linguist_sans_texte_clair():
    agent = LinguistAgent()
    state = SharedState(ciphertext="TEXTECHIFFRE")

    result = agent.analyze(state)

    assert result.status == "skipped"
    assert result.data == {}
    assert result in state.results


def test_linguist_gere_erreur(monkeypatch):
    import agents.linguist_agent as module

    def provoquer_erreur(texte):
        raise RuntimeError("Erreur de test")

    monkeypatch.setattr(module, "analyser_langue", provoquer_erreur)

    agent = LinguistAgent()
    state = SharedState(
        ciphertext="TEXTECHIFFRE",
        plaintext="BONJOUR TOUT LE MONDE"
    )

    result = agent.analyze(state)

    assert result.status == "error"
    assert "Erreur de test" in result.message
    assert result.data == {}


def test_classifier_ic_texte_trop_court():
    assert ClassifierAgent.calculate_ic("A") == 0.0


def test_classifier_ic_faible():
    agent = ClassifierAgent()
    state = SharedState(ciphertext="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    result = agent.analyze(state)

    assert result.status == "success"
    assert result.data["candidate_ciphers"] == [
        "vigenere", "autoclave"
    ]

def test_orchestrator_execution_directe(monkeypatch, capsys):
    import runpy

    runpy.run_module("agents.orchestrator", run_name="__main__")

    captured = capsys.readouterr()

    assert "ClassifierAgent" in captured.out
    assert "CryptanalystAgent" in captured.out
    assert "LinguistAgent" in captured.out
    assert "PedagogueAgent" in captured.out
    assert "Erreurs :" in captured.out

def test_pedagogue_sans_resultat_exploitable():
    agent = PedagogueAgent()
    state = SharedState(ciphertext="TEXTECHIFFRE")

    result = agent.analyze(state)

    assert result.status == "success"
    assert result.data["explanation"] == (
        "Aucun resultat exploitable n'est encore disponible."
    )
    assert result in state.results

def test_pedagogue_sans_resultat_exploitable():
    agent = PedagogueAgent()
    state = SharedState(ciphertext="TEXTECHIFFRE")

    result = agent.analyze(state)

    assert result.status == "success"
    assert result.data["explanation"] == (
        "Aucun resultat exploitable n'est encore disponible."
    )
    assert result in state.results