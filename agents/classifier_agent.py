
from collections import Counter
import re

from agents.state import SharedState, AgentResult


class ClassifierAgent:
    """Analyse statistique préliminaire du texte chiffré."""

    name = "ClassifierAgent"

    @staticmethod
    def clean(text: str) -> str:
        return re.sub(r"[^A-Z]", "", text.upper())

    @staticmethod
    def calculate_ic(text: str) -> float:
        n = len(text)
        if n < 2:
            return 0.0

        counts = Counter(text)
        total = sum(count * (count - 1) for count in counts.values())
        return total / (n * (n - 1))

    def analyze(self, state: SharedState) -> AgentResult:
        text = self.clean(state.ciphertext)

        if len(text) < 10:
            result = AgentResult(
                agent_name=self.name,
                status="error",
                message="Texte trop court pour une analyse fiable.",
                data={"length": len(text)}
            )
            state.add_result(result)
            return result

        ic = self.calculate_ic(text)

        if ic >= 0.060:
            candidates = ["cesar", "affine", "substitution"]
            explanation = "IC élevé : substitution monoalphabétique possible."
        elif ic <= 0.045:
            candidates = ["vigenere", "autoclave"]
            explanation = "IC faible : chiffrement polyalphabétique possible."
        else:
            candidates = [
                "cesar", "affine", "vigenere",
                "autoclave", "substitution", "transposition"
            ]
            explanation = "IC intermédiaire : plusieurs méthodes possibles."

        result = AgentResult(
            agent_name=self.name,
            status="success",
            message=explanation,
            data={
                "index_of_coincidence": round(ic, 5),
                "candidate_ciphers": candidates,
                "text_length": len(text)
            }
        )

        state.add_result(result)
        return result
