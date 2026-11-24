from agents.state import SharedState, AgentResult
from scripts.analyse_linguistique import analyser_langue
from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score_moyen,
)


class LinguistAgent:
    """Agent chargé d'évaluer la plausibilité linguistique."""

    name = "LinguistAgent"

    def __init__(self, quadgram_threshold: float = -4.5, language_threshold: float = 0.25):
        self.model = charger_modele()
        self.quadgram_threshold = quadgram_threshold
        self.language_threshold = language_threshold

    def analyze(self, state: SharedState) -> AgentResult:
        if not state.plaintext:
            state.is_plausible = False
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

            plausible = (
                quadgram_score > self.quadgram_threshold
                and language_score >= self.language_threshold
            )
            state.is_plausible = plausible

            if not plausible:
                state.rejection_reason = (
                    f"Texte non plausible (score quadgrammes={quadgram_score:.4f}, "
                    f"score langue={language_score:.4f}) avec la méthode '{state.cipher_type}'."
                )
                if (
                    state.cipher_type != "inconnu"
                    and state.cipher_type not in state.excluded_ciphers
                ):
                    state.excluded_ciphers.append(state.cipher_type)
            else:
                state.rejection_reason = None

            result = AgentResult(
                agent_name=self.name,
                status="success",
                message=(
                    "Analyse linguistique terminée : texte plausible."
                    if plausible
                    else f"Analyse linguistique terminée : rejeté ({state.rejection_reason})"
                ),
                data={
                    "language_score": language_score,
                    "quadgram_score": quadgram_score,
                    "is_plausible": plausible,
                    "rejection_reason": state.rejection_reason,
                }
            )

        except Exception as error:
            state.is_plausible = False
            result = AgentResult(
                agent_name=self.name,
                status="error",
                message=f"Erreur linguistique : {error}",
                data={}
            )

        state.add_result(result)
        return result