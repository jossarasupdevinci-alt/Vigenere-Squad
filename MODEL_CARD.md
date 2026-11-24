# MODEL CARD ? Vigen?re-Squad

## Vue d'ensemble
- **Syst?me** : Vigen?re-Squad (calcul d?terministe Python + pilotage LLM local Ollama).
- **Mod?les ?valu?s** :
  - Configuration (a) : Heuristique d?terministe sans LLM (`model_name=None`).
  - Configuration (b) : `llama3.2:3b` (ex?cutable sous 8 Go de RAM).
  - Configuration (c) : `qwen3:0.6b` (mod?le ultra-l?ger de comparaison).
- **Environnement de mesure** : Windows 11 (10.0.26300), Python 3.12.3, processeur AMD64.

## Limites connues et biais
1. **Sensibilit? linguistique** : Le mod?le de quadgrammes est entra?n? sur le fran?ais (`data/corpus_francais.txt`), entra?nant un taux de succ?s de 0 % sur le corpus anglais sans changement de table n-grammes.
2. **Sensibilit? au bruit** : Avec 5 % d'alt?rations de caract?res, l'?galit? stricte (`taux_clair_exact`) chute ? 0 % bien que le texte reste partiellement lisible.
3. **Co?t temporel des LLM locaux** : L'appel aux mod?les locaux ajoute ~9,5 ? 10,2 s par message sur CPU par rapport ? la base d?terministe (25,55 s vs 35,05?35,80 s).

## S?curit? (Analyse STRIDE)
- **Hallucination d'outils** : Contr?le strict de liste ferm?e (`OUTILS_CRYPTANALYSTE`) rejetant tout nom d'outil non autoris?.
- **Injection de prompt via texte chiffr?** : Seuls les indicateurs num?riques (IC, longueur) sont transmis au LLM, jamais le texte chiffr? brut.
- **D?ni de service (boucles infinies)** : Plafonnement strict via `max_iterations` et `max_retries` dans `Orchestrator`.
