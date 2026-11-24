import json
import urllib.request
import urllib.error
from pathlib import Path


OLLAMA_URL = "http://localhost:11434/api/generate"


def charger_prompt(nom_fichier: str) -> str:
    chemin = Path("prompts") / nom_fichier
    if chemin.exists():
        return chemin.read_text(encoding="utf-8")
    return ""


def interroger_ollama_json(
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    outils_autorises: list[str] | None = None,
    temperature: float = 0.0,
    timeout: float = 15.0,
) -> dict:
    """
    Interroge Ollama en local avec sortie JSON forcée et contrôle de liste fermée d'outils.
    Lève une RuntimeError en cas d'échec réseau, de JSON invalide ou d'outil non autorisé.
    """
    payload = {
        "model": model_name,
        "system": system_prompt,
        "prompt": user_prompt,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": temperature,
            "seed": 42,
            "num_ctx": 4096,
        },
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Erreur appel Ollama ({model_name}) : {exc}") from exc

    raw_response = body.get("response", "").strip()
    if not raw_response:
        raise RuntimeError("Réponse vide renvoyée par le modèle local.")

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Sortie JSON invalide : {raw_response[:120]}") from exc

    if not isinstance(parsed, dict):
        raise RuntimeError("La sortie JSON n'est pas un objet dictionnaire.")

    # Contrôle strict de la liste fermée d'outils (contre-mesure hallucination)
    if outils_autorises is not None and "outil_choisi" in parsed:
        outil = parsed["outil_choisi"]
        if outil not in outils_autorises:
            raise RuntimeError(
                f"Appel d'outil non autorisé ou halluciné : '{outil}' "
                f"(autorisés : {outils_autorises})"
            )

    return parsed
