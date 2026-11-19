
from agents.state import SharedState, AgentResult


class PedagogueAgent:
    """Agent chargé d'expliquer les résultats des analyses."""

    name = "PedagogueAgent"

    def analyze(self, state: SharedState) -> AgentResult:
        explanations = []

        if state.cipher_type != "inconnu":
            explanations.append(
                f"Methode de chiffrement envisagee : {state.cipher_type}."
            )

        for result in state.results:
            if result.agent_name == "ClassifierAgent":
                ic = result.data.get("index_of_coincidence")
                if ic is not None:
                    explanations.append(
                        f"L'indice de coincidence mesure la repetition "
                        f"des lettres. Sa valeur est {ic:.5f}."
                    )

                candidates = result.data.get("candidate_ciphers", [])
                if candidates:
                    explanations.append(
                        "Les methodes candidates sont : "
                        + ", ".join(candidates) + "."
                    )

            elif result.agent_name == "CryptanalystAgent":
                explanations.append(
                    "L'analyse cryptographique a recherche des repetitions "
                    "et calcule l'indice de coincidence."
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
                        "Il permet de comparer la plausibilite du texte "
                        "avec le modele linguistique."
                    )

        explanation = " ".join(explanations)

        if not explanation:
            explanation = (
                "Aucun resultat exploitable n'est encore disponible."
            )

        result = AgentResult(
            agent_name=self.name,
            status="success",
            message="Explication pédagogique générée.",
            data={"explanation": explanation}
        )

        state.add_result(result)
        return result
