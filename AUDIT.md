# Rapport d'Audit — Vigenere-Squad

**Version auditée** : 1.0.0
**Date** : 2026-11-19

## 1. Résultats des tests

| Métrique | Valeur |
|---|---|
| Tests exécutés | 95 |
| Tests réussis | 95 |
| Couverture globale | 82 % |
| Module à 100 % | chiffrement_autoclave.py |

## 2. Points d'amélioration

| Fichier | Observation |
|---|---|
| scripts/hello.py | Fichier résiduel, à supprimer |
| scripts/chiffrement_cesar.py | Définition double de chiffrer_cesar |
| scripts/analyse_linguistique.py | Vocabulaire limité (34 mots) |

## 3. CI/CD

GitHub Actions opérationnel sur push et pull_request vers main. pytest-cov ajouté.

## 4. Conclusion

95/95 tests passent. Projet prêt pour release v1.0.0.
