from agents.state import SharedState, AgentResult
from agents.llm_client import charger_prompt, interroger_ollama_json

from scripts.indice_coincidence import calculer_indice_coincidence
from scripts.kasiski import analyser_kasiski
from scripts.force_brute_cesar import force_brute_cesar
from scripts.chiffrement_affine import dechiffrer_affine
from scripts.attaque_substitution import recuit_simule
from scripts.attaque_vigenere import attaquer_vigenere
from scripts.attaque_autoclave import attaquer_autoclave

from scripts.score_quadgrammes import (
    charger_modele,
    calculer_score_moyen,
)


OUTILS_CRYPTANALYSTE = [
    "force_brute_cesar",
    "dechiffrer_affine",
    "attaquer_vigenere",
    "attaquer_autoclave",
    "recuit_simule",
]


class CryptanalystAgent:
    name = "CryptanalystAgent"

    def __init__(self, model_name: str | None = None):
        self.model = charger_modele()
        self.model_name = model_name
        self.system_prompt = charger_prompt("cryptanalyst_v1.md")

    def _demander_decision_llm(self, ic: float, longueur: int, excluded: set[str], rejection: str | None) -> dict | None:
        if not self.model_name:
            return None
        user_msg = (
            f"Indice de coïncidence (IC) = {ic:.5f}, longueur du texte = {longueur} caractères.\n"
            f"Procédés déjà exclus par le Linguiste : {sorted(excluded)}.\n"
            f"Raison du dernier rejet : {rejection or 'Aucun rejet (1er essai)'}.\n"
            f"Choisis l'outil le plus pertinent parmi : {OUTILS_CRYPTANALYSTE}."
        )
        return interroger_ollama_json(
            model_name=self.model_name,
            system_prompt=self.system_prompt,
            user_prompt=user_msg,
            outils_autorises=OUTILS_CRYPTANALYSTE,
            timeout=30.0,
        )

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
            excluded = set(state.excluded_ciphers)

            llm_decision = None
            llm_error = None
            if self.model_name:
                try:
                    llm_decision = self._demander_decision_llm(
                        ic, len(text), excluded, state.rejection_reason
                    )
                except Exception as exc:
                    llm_error = str(exc)

            best_score = float("-inf")
            best_text = None
            best_key = None
            best_type = None

            cesar_candidates = {}
            vigenere_result = None
            vigenere_error = None
            autoclave_result = None
            autoclave_error = None

            outil_prioritaire = llm_decision.get("outil_choisi") if llm_decision else None

            def tester_cesar():
                nonlocal best_score, best_text, best_key, best_type, cesar_candidates
                if "cesar" in excluded:
                    return
                cesar_candidates = force_brute_cesar(state.ciphertext)
                for key, candidate in cesar_candidates.items():
                    score = calculer_score_moyen(candidate, self.model)
                    if score > best_score:
                        best_score = score
                        best_text = candidate
                        best_key = key
                        best_type = "cesar"

            def tester_affine():
                nonlocal best_score, best_text, best_key, best_type
                if "affine" in excluded:
                    return
                valeurs_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
                for a in valeurs_a:
                    for b in range(26):
                        candidate = dechiffrer_affine(state.ciphertext, a, b)
                        score = calculer_score_moyen(candidate, self.model)
                        if score > best_score:
                            best_score = score
                            best_text = candidate
                            best_key = {"a": a, "b": b}
                            best_type = "affine"

            def tester_substitution():
                nonlocal best_score, best_text, best_key, best_type
                if "substitution" in excluded or len(text) < 500:
                    return
                substitution_key, substitution_text, substitution_score = (
                    recuit_simule(
                        state.ciphertext,
                        self.model,
                        iterations=50000,
                        graine=42
                    )
                )
                if substitution_score > best_score:
                    best_score = substitution_score
                    best_text = substitution_text
                    best_key = substitution_key
                    best_type = "substitution"

            def tester_vigenere():
                nonlocal best_score, best_text, best_key, best_type, vigenere_result, vigenere_error
                if "vigenere" in excluded or len(text) < 20:
                    return
                try:
                    vigenere_result = attaquer_vigenere(state.ciphertext, self.model)
                    if vigenere_result["score"] > best_score:
                        best_score = vigenere_result["score"]
                        best_text = vigenere_result["texte_clair"]
                        best_key = vigenere_result["cle"]
                        best_type = "vigenere"
                except Exception as error:
                    vigenere_error = str(error)

            def tester_autoclave():
                nonlocal best_score, best_text, best_key, best_type, autoclave_result, autoclave_error
                if "autoclave" in excluded or len(text) < 20:
                    return
                try:
                    autoclave_result = attaquer_autoclave(state.ciphertext, self.model)
                    if autoclave_result["score"] > best_score:
                        best_score = autoclave_result["score"]
                        best_text = autoclave_result["texte_clair"]
                        best_key = autoclave_result["cle"]
                        best_type = "autoclave"
                except Exception as error:
                    autoclave_error = str(error)

            actions = {
                "force_brute_cesar": tester_cesar,
                "dechiffrer_affine": tester_affine,
                "recuit_simule": tester_substitution,
                "attaquer_vigenere": tester_vigenere,
                "attaquer_autoclave": tester_autoclave,
            }

            if outil_prioritaire in actions:
                actions[outil_prioritaire]()
                if best_score <= -3.2:
                    for nom_outil, fn in actions.items():
                        if nom_outil != outil_prioritaire:
                            fn()
            else:
                for fn in actions.values():
                    fn()

            state.plaintext = best_text
            state.candidate_key = str(best_key) if best_key is not None else None
            state.cipher_type = best_type if best_type is not None else "inconnu"

            if best_type in ("vigenere", "autoclave") and isinstance(best_key, str):
                state.estimated_key_length = len(best_key)

            analyses = {
                "model_name": self.model_name,
                "llm_decision": llm_decision,
                "llm_error": llm_error,
                "index_of_coincidence": ic,
                "kasiski": kasiski_result,
                "text_length": len(text),
                "excluded_ciphers": list(excluded),
                "detected_cipher": best_type,
                "candidate_key": best_key,
                "best_candidate": best_text,
                "quadgram_score": best_score,
                "cesar_candidates_tested": len(cesar_candidates),
                "affine_candidates_tested": 312 if "affine" not in excluded else 0,
                "substitution_iterations": 50000 if ("substitution" not in excluded and len(text) >= 500) else 0,
                "vigenere_result": vigenere_result,
                "vigenere_error": vigenere_error,
                "vigenere_key_length": (
                    vigenere_result["longueur_cle"]
                    if vigenere_result else None
                ),
                "autoclave_result": autoclave_result,
                "autoclave_error": autoclave_error,
            }

            result = AgentResult(
                agent_name=self.name,
                status="success",
                message=(
                    f"Analyses exécutées (mode={'LLM ' + self.model_name if self.model_name else 'déterministe'})."
                ),
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
