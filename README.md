# Vigenère-Squad — Cryptanalyse Multi-Agents Locale

Système multi-agents de cryptanalyse classique (César, Affine, Substitution monoalphabétique, Vigenère, Autoclave, Transposition) alliant des **outils cryptanalytiques déterministes** (Python) et une **orchestration par modèles de langage locaux** (Ollama).

## Architecture

- **ClassifierAgent** : calcule l'indice de coïncidence (IC) et les fréquences pour orienter vers les familles monoalphabétiques ou polyalphabétiques.
- **CryptanalystAgent** : sélectionne l'attaque adaptée (force brute César, affine, recuit simulé sur quadgrammes, Vigenère par décalages, attaque autoclave dédiée) via une liste fermée d'outils et un contrat JSON strict.
- **LinguistAgent** : évalue la plausibilité linguistique (log-probabilité des quadgrammes français) et déclenche une boucle de rejet/correction en cas de faux positif.
- **PedagogueAgent** : génère une explication pas à pas et un exercice similaire avec corrigé.

## Prérequis et Installation

- Python 3.12+ : `python -m pip install -r requirements.txt`
- Ollama installé localement : `ollama pull llama3.2:3b` et `ollama pull qwen3:0.6b`

## Commandes de reproduction

- **Exécuter les 122 tests unitaires et de défaillance :** `python -m pytest`
- **Reproduire rapidement les expériences (`results/metrics.json`) :** `python -m scripts.executer_experiences --small`
- **Lancer l'expérience complète (3 répétitions) :** `python -m scripts.executer_experiences`
- **Lancer l'interface de démonstration Streamlit :** `python -m streamlit run app.py`
