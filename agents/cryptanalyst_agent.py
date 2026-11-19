
from agents.state import SharedState, AgentResult

from scripts.indice_coincidence import calculer_indice_coincidence
from scripts.kasiski import analyser_kasiski
from scripts.force_brute_cesar import force_brute_cesar
from scripts.chiffrement_affine import dechiffrer_affine
from scripts.attaque_substitution import recuit_simule
from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score_moyen,
)


class CryptanalystAgent:
    name = "CryptanalystAgent"

    def __init__(self):
        self.model = charger_modele()

    def analyze(self, state: SharedState) -> AgentResult:
        text = "".join(
            char for char in state.ciphertext.upper()
            if "A" <= char <= "Z"
        )

        if len(text) < 10:
            result = AgentResult(
                agent_name=self.name,
                status="error",
                message="Texte trop court pour une analyse fiable.",
                data={"text_length": len(text)}
            )
            state.add_result(result)
            return result

        try:
            ic = calculer_indice_coincidence(text)
            kasiski_result = analyser_kasiski(text)

            best_score = float("-inf")
            best_text = None
            best_key = None
            best_type = None

            # 1. Attaque César
            cesar_candidates = force_brute_cesar(state.ciphertext)

            for key, candidate in cesar_candidates.items():
                score = calculer_score_moyen(candidate, self.model)

                if score > best_score:
                    best_score = score
                    best_text = candidate
                    best_key = key
                    best_type = "cesar"

            # 2. Attaque affine
            valeurs_a = [
                1, 3, 5, 7, 9, 11,
                15, 17, 19, 21, 23, 25
            ]

            for a in valeurs_a:
                for b in range(26):
                    candidate = dechiffrer_affine(
                        state.ciphertext, a, b
                    )
                    score = calculer_score_moyen(
                        candidate, self.model
                    )

                    if score > best_score:
                        best_score = score
                        best_text = candidate
                        best_key = {"a": a, "b": b}
                        best_type = "affine"

            # 3. Attaque par substitution
            substitution_key, substitution_text, substitution_score = (
                recuit_simule(
                    state.ciphertext,
                    self.model,
                    iterations=100000,
                    graine=42
                )
            )

            if len(text) >= 500 and substitution_score > best_score:
                best_score = substitution_score
                best_text = substitution_text
                best_key = substitution_key
                best_type = "substitution"

            state.plaintext = best_text
            state.candidate_key = str(best_key)
            state.cipher_type = best_type

            analyses = {
                "index_of_coincidence": ic,
                "kasiski": kasiski_result,
                "text_length": len(text),
                "detected_cipher": best_type,
                "candidate_key": best_key,
                "best_candidate": best_text,
                "quadgram_score": best_score,
                "cesar_candidates_tested": len(cesar_candidates),
                "affine_candidates_tested": 312,
                "substitution_iterations": 100000,
            }

            result = AgentResult(
                agent_name=self.name,
                status="success",
                message="Attaques César, affine et substitution exécutées.",
                data=analyses
            )

        except Exception as error:
            result = AgentResult(
                agent_name=self.name,
                status="error",
                message=f"Erreur pendant l'analyse : {error}",
                data={}
            )

        state.add_result(result)
        return result
