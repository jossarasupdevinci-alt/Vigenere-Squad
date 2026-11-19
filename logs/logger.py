
import json
from pathlib import Path
from agents.state import SharedState


class AgentLogger:
    def __init__(self, log_path="logs/agent_traces.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, state: SharedState) -> None:
        entry = state.to_dict()

        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(entry, ensure_ascii=False, default=str) + "\n"
            )
