
from dataclasses import dataclass, field
from typing import Any, Literal


CipherType = Literal[
    "cesar",
    "affine",
    "vigenere",
    "autoclave",
    "substitution",
    "transposition",
    "inconnu",
]


@dataclass
class AgentResult:
    agent_name: str
    status: Literal["success", "error", "skipped"]
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class SharedState:
    ciphertext: str
    language: str = "fr"
    cipher_type: CipherType = "inconnu"
    confidence: float = 0.0
    estimated_key_length: int | None = None
    candidate_key: str | None = None
    plaintext: str | None = None
    results: list[AgentResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_result(self, result: AgentResult) -> None:
        self.results.append(result)

    def add_error(self, error: str) -> None:
        self.errors.append(error)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ciphertext": self.ciphertext,
            "language": self.language,
            "cipher_type": self.cipher_type,
            "confidence": self.confidence,
            "estimated_key_length": self.estimated_key_length,
            "candidate_key": self.candidate_key,
            "plaintext": self.plaintext,
            "results": [
                {
                    "agent_name": result.agent_name,
                    "status": result.status,
                    "message": result.message,
                    "data": result.data,
                }
                for result in self.results
            ],
            "errors": self.errors,
        }
