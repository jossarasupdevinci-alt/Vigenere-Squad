# Déclaration d'usage de l'IA — Vigenere-Squad

**Version** : 1.0.0  
**Date** : 2026-11-19  

---

## 1. Outils d'IA utilisés

| Outil | Usage | Volume estimé |
|---|---|---|
| Claude (Anthropic) | Génération de documentation, revue de code, aide à la rédaction du rapport | Modéré |
| GitHub Copilot | Complétion de code lors du développement | Faible |

---

## 2. Ce qui a été généré par l'IA

- Squelettes de docstrings complétés manuellement.
- Suggestions de cas de test revues et adaptées par l'équipe.
- Parties de la documentation (SYSTEM_CARD, AUDIT, ce fichier) rédigées avec assistance IA puis relues.

---

## 3. Ce qui n'a pas été généré par l'IA

- La logique cryptographique (algorithmes de chiffrement/déchiffrement) : implémentée manuellement.
- Les tests unitaires : écrits par l'équipe, avec vérification manuelle des assertions.
- Le corpus de textes : généré par `generer_corpus.py`, script écrit par l'équipe.
- L'architecture multi-agents : conçue et implémentée par l'équipe.

---

## 4. Politique de validation

Tout code ou texte généré ou suggéré par un outil d'IA a été :
1. Lu et compris par au moins un membre de l'équipe.
2. Testé (pour le code) ou relu (pour la documentation).
3. Modifié si nécessaire avant intégration.

---

## 5. Conformité

Ce projet respecte la politique d'usage de l'IA de l'établissement : l'IA est utilisée comme outil d'assistance, non comme substitut au travail de l'équipe. L'équipe reste responsable de l'intégralité du contenu livré.