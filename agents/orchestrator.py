
from agents.state import SharedState, AgentResult
from agents.classifier_agent import ClassifierAgent
from agents.cryptanalyst_agent import CryptanalystAgent
from agents.linguist_agent import LinguistAgent
from agents.pedagogue_agent import PedagogueAgent
from agents.logger import AgentLogger


class Orchestrator:
    """Coordonne les agents de Vigenere-Squad."""

    def __init__(self):
        self.classifier = ClassifierAgent()
        self.cryptanalyst = CryptanalystAgent()
        self.linguist = LinguistAgent()
        self.pedagogue = PedagogueAgent()
        self.logger = AgentLogger()

    def run(self, ciphertext: str) -> SharedState:
        state = SharedState(ciphertext=ciphertext)

        agents = [
            self.classifier,
            self.cryptanalyst,
            self.linguist,
            self.pedagogue,
        ]

        for agent in agents:
            try:
                agent.analyze(state)
            except Exception as error:
                state.add_result(AgentResult(
                    agent_name=agent.name,
                    status="error",
                    message=str(error),
                    data={}
                ))
                state.add_error(f"{agent.name}: {error}")

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
