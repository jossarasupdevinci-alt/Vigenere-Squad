from agents.state import SharedState, AgentResult
from agents.classifier_agent import ClassifierAgent
from agents.cryptanalyst_agent import CryptanalystAgent
from agents.linguist_agent import LinguistAgent
from agents.pedagogue_agent import PedagogueAgent
from agents.logger import AgentLogger


class Orchestrator:
    """Coordonne les agents de Vigenere-Squad avec boucle de vérification."""

    def __init__(self, model_name: str | None = None, max_iterations: int = 3, max_retries: int = 2):
        self.model_name = model_name
        self.classifier = ClassifierAgent()
        self.cryptanalyst = CryptanalystAgent(model_name=model_name)
        self.linguist = LinguistAgent()
        self.pedagogue = PedagogueAgent()
        self.logger = AgentLogger()
        self.max_iterations = max_iterations
        self.max_retries = max_retries

    def _run_with_retry(self, agent, state: SharedState) -> AgentResult | None:
        """Exécute un agent avec tentatives de repli en cas d'erreur."""
        last_error = None
        for _ in range(self.max_retries):
            try:
                res = agent.analyze(state)
                if res.status != "error":
                    return res
                last_error = res.message
            except Exception as error:
                last_error = str(error)
                state.add_result(AgentResult(
                    agent_name=agent.name,
                    status="error",
                    message=str(error),
                    data={}
                ))
        if last_error:
            state.add_error(f"{agent.name}: {last_error}")
        return None

    def run(self, ciphertext: str) -> SharedState:
        state = SharedState(ciphertext=ciphertext)

        # 1. Classification initiale
        self._run_with_retry(self.classifier, state)

        # 2. Boucle de correction Cryptanalyste <-> Linguiste
        for iteration in range(1, self.max_iterations + 1):
            state.iteration_count = iteration
            crypto_res = self._run_with_retry(self.cryptanalyst, state)
            linguist_res = self._run_with_retry(self.linguist, state)

            if crypto_res is None or not state.plaintext:
                break
            if linguist_res is not None and state.is_plausible:
                break

        # 3. Explication pédagogique (et génération d'un exercice similaire)
        pedagogue_res = self._run_with_retry(self.pedagogue, state)
        if pedagogue_res is not None and state.cipher_type != "inconnu":
            try:
                exo = self.pedagogue.generer_exercice(
                    methode=state.cipher_type,
                    seed=42
                )
                pedagogue_res.data["exercice"] = exo
            except Exception as error:
                state.add_error(f"PedagogueAgent (exercice): {error}")

        self.logger.log(state)
        return state


if __name__ == "__main__":
    sample = (
        "BONJOURTOUTLEMONDECECI EST UN TEXTE "
        "DE TEST POUR VIGENERE SQUAD"
    )

    orchestrator = Orchestrator()
    result = orchestrator.run(sample)

    for agent_result in result.results:
        print(
            agent_result.agent_name,
            agent_result.status,
            agent_result.message
        )

    print("\nErreurs :", result.errors)
