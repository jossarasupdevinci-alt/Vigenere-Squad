
from agents.state import SharedState, AgentResult
from scripts.analyse_linguistique import analyser_langue
from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score_moyen,
)


class LinguistAgent:
    """Agent chargé d'évaluer la plausibilité linguistique."""

    name = "LinguistAgent"

    def __init__(self):
        self.model = charger_modele()

    def analyze(self, state: SharedState) -> AgentResult:
        if not state.plaintext:
            result = AgentResult(
                agent_name=self.name,
                status="skipped",
                message="Aucun texte clair disponible à analyser.",
                data={}
            )
            state.add_result(result)
            return result

        try:
            language_score = analyser_langue(state.plaintext)
            quadgram_score = calculer_score_moyen(
                state.plaintext,
                self.model
            )

            result = AgentResult(
                agent_name=self.name,
                status="success",
                message="Analyse linguistique terminée.",
                data={
                    "language_score": language_score,
                    "quadgram_score": quadgram_score,
                }
            )

        except Exception as error:
            result = AgentResult(
                agent_name=self.name,
                status="error",
                message=f"Erreur linguistique : {error}",
                data={}
            )

        state.add_result(result)
        return result
