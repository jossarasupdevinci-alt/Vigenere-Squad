# Rapport d'Audit — Vigenere-Squad

**Version auditée** : 1.0.0  
**Date** : 2026-11-19  
**Auditeurs** : Équipe Vigenere-Squad  

---

## 1. Périmètre de l'audit

L'audit couvre :
- Le code source des scripts cryptographiques (`scripts/`)
- La suite de tests automatisés (`tests/`)
- Le pipeline CI/CD (`.github/workflows/`)
- Le corpus de données (`data/`)

---

## 2. Résultats des tests automatisés

| Métrique | Valeur |
|---|---|
| Tests exécutés | 95 |
| Tests réussis | 95 |
| Tests échoués | 0 |
| Couverture globale | 82 % |
| Module à 100 % | `chiffrement_autoclave.py` |
| Modules > 95 % | `entrainer_quadgrammes.py` (98 %), `telecharger_corpus.py` (98 %), `chiffrement_transposition.py` (97 %) |

---

## 3. Analyse de la qualité du code

### 3.1 Points forts

- Séparation claire entre logique de chiffrement et logique d'attaque.
- Chaque module expose des fonctions nommées de manière cohérente (`chiffrer_X`, `dechiffrer_X`).
- Les erreurs métier sont levées via des exceptions explicites (`ValueError`).
- Le corpus est généré de manière reproductible.

### 3.2 Points d'amélioration identifiés

| Fichier | Observation | Priorité |
|---|---|---|
| `scripts/hello.py` | Fichier de test résiduel, couverture 0 %, à supprimer ou documenter | Faible |
| `scripts/chiffrement_cesar.py` | Définition de `chiffrer_cesar` en double dans le fichier | Moyenne |
| `scripts/analyse_linguistique.py` | Vocabulaire de référence limité (34 mots) ; étendre pour améliorer la précision | Moyenne |
| `scripts/score_quadgrammes.py` | Couverture 71 % ; cas limites non testés | Faible |

---

## 4. Vérification du corpus

| Critère | Valeur attendue | Valeur mesurée | Statut |
|---|---|---|---|
| Nombre de textes | ≥ 150 | 150 | ✅ |
| Méthodes de chiffrement | 6 | 6 | ✅ |
| Longueurs variées | Oui | Oui (courts, moyens, longs) | ✅ |

---

## 5. Vérification des expériences

| Expérience | Répétitions | Résultat | Statut |
|---|---|---|---|
| Précision force brute César | 3 | 100 % | ✅ |
| Indice de coïncidence par méthode | 3 | Mesuré pour 4 méthodes | ✅ |
| Score linguistique après déchiffrement | 3 | Calculé | ✅ |
| Robustesse Kasiski | 3 | Testé pour 5 longueurs de clé | ✅ |

---

## 6. Vérification de la boucle de correction

La boucle de correction est implémentée au niveau de l'orchestrateur : si le score linguistique du texte déchiffré est inférieur à un seuil (0.3), l'orchestrateur relance l'agent Cryptanalyst avec une hypothèse différente.

**Scénarios de panne des outils testés** :
- Texte vide → `ValueError` levée correctement
- Texte trop court pour Kasiski → `ValueError` levée correctement
- Clé affine avec `pgcd(a, 26) ≠ 1` → `ValueError` levée correctement

---

## 7. Vérification du CI/CD

- Workflow GitHub Actions opérationnel sur `push` et `pull_request` vers `main`.
- Python 3.12 utilisé en CI.
- `pytest-cov` ajouté pour mesure automatique de la couverture.

---

## 8. Conclusion

Le projet Vigenere-Squad est en bon état pour une release v1.0.0. Les 95 tests passent, le corpus est complet, et les expériences de robustesse ont été réalisées en 3 répétitions. Les points d'amélioration identifiés sont mineurs et n'affectent pas la fonctionnalité principale.