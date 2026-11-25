# Rapport Technique — Vigenère-Squad
## Architecture hybride déterministe et LLM locaux (Ollama)

**Version** : 1.0.0  
**Date de mesure** : 2026-11-24  
**OS** : Windows 11 | **Python** : 3.12.3 | **Corpus** : 150 messages  

---

## 1. Contexte et Architecture Multi-Agents

Le projet Vigenère-Squad implémente une architecture multi-agents locale destinée à l'analyse et au déchiffrement de procédés cryptographiques classiques (César, Affine, Substitution monoalphabétique, Vigenère, Autoclave, Transposition). Les calculs mathématiques et statistiques sont exécutés par des outils Python déterministes, tandis que les modèles locaux (Ollama) assurent le choix stratégique d'outils et la justification pédagogique.

- **ClassifierAgent** : calcule l'indice de coïncidence (IC) et les fréquences pour orienter vers les familles monoalphabétiques ou polyalphabétiques.
- **CryptanalystAgent** : sélectionne et exécute l'attaque appropriée via une liste fermée d'outils et un contrat JSON strict.
- **LinguistAgent** : évalue la plausibilité linguistique (log-probabilité des quadgrammes français) et déclenche une boucle de rejet/correction en cas de faux positif.
- **PedagogueAgent** : rédige une explication étape par étape et génère un exercice similaire avec corrigé.

---

## 2. Environnement Expérimental et Reproductibilité

La base de code est validée par **122 tests unitaires et tests de défaillance** (pytest). Les prompts système sont versionnés dans `prompts/` avec suivi dans `CHANGELOG.md`.

**Commandes de reproduction :**

```bash
# Exécuter les 122 tests
python -m pytest

# Reproduire rapidement les expériences
python -m scripts.executer_experiences --small

# Lancer l'expérience complète (3 répétitions)
python -m scripts.executer_experiences

# Lancer l'interface de démonstration Streamlit
python -m streamlit run app.py
```

---

## 3. Preuve Expérimentale : Chiffre Autoclave vs Test de Kasiski

Sur 10 messages chiffrés par procédé Autoclave, le test de Kasiski obtient **0.0 % de réussite** contre **90.0 %** pour l'attaque Autoclave dédiée.

| Méthode évaluée | Échantillons | Taux de réussite (%) |
|---|---|---|
| Test de Kasiski seul | 10 | 0.0 % |
| Attaque Autoclave dédiée | 10 | 90.0 % |

---

## 4. Étude d'Ablation (3 Configurations)

| Configuration | Modèle | Taux clair exact (%) | Temps moyen / msg (s) |
|---|---|---|---|
| a_sans_llm_deterministe | aucun (heuristique) | 16.67 % | 42.14 s |
| b_llm_8go_llama3_2_3b | llama3.2:3b | 16.67 % | 47.80 s |
| c_llm_leger_qwen3_0_6b | qwen3:0.6b | 16.67 % | 49.65 s |

---

## 5. Étude de Robustesse

| Scénario de dégradation | Taux clair exact (%) | Temps moyen (s) |
|---|---|---|
| sans_espaces_ni_ponctuation | 50.0 % | 29.48 s |
| avec_5pct_fautes | 0.0 % | 29.96 s |
| corpus_anglais | 0.0 % | 2.90 s |

---

## 6. Validation Empirique de la Distance d'Unicité de Shannon

La distance d'unicité théorique `U = (L × log2(26)) / 3,2` représente la borne inférieure d'information. En pratique, l'attaque statistique par colonnes exige 25 à 85 fois plus de caractères (180 à 500 lettres).

| Longueur clé L | Distance unicité théorique (car.) | Seuil empirique ≥ 90 % (car.) |
|---|---|---|
| 3 | 4.41 | 180 |
| 4 | 5.88 | 500 |
| 5 | 7.34 | 250 |
| 6 | 8.81 | 500 |
| 7 | 10.28 | 250 |
| 8 | 11.75 | 500 |
| 9 | 13.22 | 500 |
| 10 | 14.69 | 500 |

---

## 7. Analyse de Sécurité (STRIDE) et Limites

- **Usurpation / Hallucination d'outils** : rejet systématique hors de la liste fermée `OUTILS_CRYPTANALYSTE`.
- **Injection de prompt via texte chiffré** : seuls des indicateurs numériques (IC, longueur) sont transmis au LLM.
- **Déni de service (boucles infinies)** : bornage strict par `max_iterations` et `max_retries`.
- **Limites** : dépendance à la langue française des quadgrammes, sensibilité aux textes courts et latence CPU des LLM locaux.

---

*Rapport généré le 2026-11-24 — Équipe Vigenère-Squad*
