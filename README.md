# Vigen?re-Squad ? Cryptanalyse Multi-Agents Locale

Syst?me multi-agents de cryptanalyse classique (C?sar, Affine, Substitution monoalphab?tique, Vigen?re, Autoclave, Transposition) alliant des **outils cryptanalytiques d?terministes** (Python) et une **orchestration par mod?les de langage locaux** (Ollama).

## Architecture

- **ClassifierAgent** : calcule l'indice de co?ncidence (IC) et les fr?quences pour orienter vers les familles monoalphab?tiques ou polyalphab?tiques.
- **CryptanalystAgent** : s?lectionne l'attaque adapt?e (force brute C?sar, affine, recuit simul? sur quadgrammes, Vigen?re par d?calages, attaque autoclave d?di?e) via une liste ferm?e d'outils et un contrat JSON strict.
- **LinguistAgent** : ?value la plausibilit? linguistique (log-probabilit? des quadgrammes fran?ais) et d?clenche une boucle de rejet/correction en cas de faux positif.
- **PedagogueAgent** : g?n?re une explication pas ? pas et un exercice similaire avec corrig?.

## Pr?requis et Installation

- Python 3.12+ : `python -m pip install -r requirements.txt`
- Ollama install? localement : `ollama pull llama3.2:3b` et `ollama pull qwen3:0.6b`

## Commandes de reproduction

- **Ex?cuter les 122 tests unitaires et de d?faillance :** `python -m pytest`
- **Reproduire rapidement les exp?riences (`results/metrics.json`) :** `python -m scripts.executer_experiences --small`
- **Lancer l'exp?rience compl?te (3 r?p?titions) :** `python -m scripts.executer_experiences`
- **Lancer l'interface de d?monstration Streamlit :** `python -m streamlit run app.py`
