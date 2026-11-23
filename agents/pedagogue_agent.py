
from typing import Any

from agents.state import SharedState, AgentResult
from agents.exercise_generator import generer_exercice, METHODES
from agents.exercise_checker import verifier_reponse


class PedagogueAgent:
    """Agent chargé d'expliquer les analyses et de proposer des exercices."""

    name = "PedagogueAgent"

    def __init__(self):
        self.exercice_en_cours = None

    def analyze(self, state: SharedState) -> AgentResult:
        explanations = []

        if state.cipher_type != "inconnu":
            explanations.append(
                f"Méthode de chiffrement envisagée : {state.cipher_type}."
            )

        for result in state.results:
            if result.agent_name == "ClassifierAgent":
                ic = result.data.get("index_of_coincidence")
                if ic is not None:
                    explanations.append(
                        f"L'indice de coïncidence mesure la répétition "
                        f"des lettres. Sa valeur est {ic:.5f}."
                    )

                candidates = result.data.get("candidate_ciphers", [])
                if candidates:
                    explanations.append(
                        "Les méthodes candidates sont : "
                        + ", ".join(candidates) + "."
                    )

            elif result.agent_name == "CryptanalystAgent":
                explanations.append(
                    "L'analyse cryptographique a recherché des répétitions "
                    "et calculé l'indice de coïncidence."
                )

            elif result.agent_name == "LinguistAgent":
                language_score = result.data.get("language_score")
                quadgram_score = result.data.get("quadgram_score")

                if language_score is not None:
                    explanations.append(
                        f"Le score linguistique est {language_score:.4f}."
                    )

                if quadgram_score is not None:
                    explanations.append(
                        f"Le score quadgrammes est {quadgram_score:.4f}. "
                        "Il permet de comparer la plausibilité du texte "
                        "avec le modèle linguistique."
                    )

        explanation = " ".join(explanations)

        if not explanation:
            explanation = (
                "Aucun résultat exploitable n'est encore disponible."
            )

        result = AgentResult(
            agent_name=self.name,
            status="success",
            message="Explication pédagogique générée.",
            data={"explanation": explanation}
        )

        state.add_result(result)
        return result

    def generer_exercice(
        self,
        methode: str | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """Génère un exercice et conserve sa solution en interne."""

        exercice = generer_exercice(methode=methode, seed=seed)
        self.exercice_en_cours = exercice

        return exercice.enonce

    def corriger_reponse(self, texte_propose: str) -> dict[str, Any]:
        """Corrige la réponse à l'exercice en cours."""

        if self.exercice_en_cours is None:
            raise ValueError(
                "Aucun exercice n'a été généré pour le moment."
            )

        return verifier_reponse(
            texte_propose,
            self.exercice_en_cours.solution
        )
