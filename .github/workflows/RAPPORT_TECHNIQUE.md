# Rapport Technique — Vigenere-Squad
## Système multi-agents de cryptanalyse classique

**Version** : 1.0.0  
**Date** : 2026-11-19  
**Projet** : TP Vigenere-Squad — Cryptanalyse et agents IA  

---

## Table des matières

1. Introduction et objectifs
2. Architecture du système
3. Outils cryptographiques implémentés
4. Corpus et données
5. Méthodes d'attaque cryptanalytique
6. Expérimentations et résultats
7. Analyse de sécurité (STRIDE)
8. Tests et qualité
9. Limitations et travaux futurs
10. Conclusion

---

## 1. Introduction et objectifs

Vigenere-Squad est un système multi-agents conçu pour analyser, attaquer et déchiffrer des messages chiffrés avec des algorithmes de cryptographie classique. Le projet s'inscrit dans le cadre d'un TP de sécurité de l'information visant à illustrer les principes fondamentaux de la cryptanalyse à travers une architecture logicielle modulaire.

### Objectifs

- Implémenter six méthodes de chiffrement classique.
- Concevoir une architecture multi-agents capable de coordonner des tâches d'analyse.
- Réaliser des attaques cryptanalytiques sur un corpus de 150 textes en français.
- Évaluer la robustesse des chiffrements face aux attaques implémentées.
- Produire une documentation complète (audit, système card, usage IA).

---

## 2. Architecture du système

Le système repose sur un **orchestrateur central** qui coordonne quatre agents spécialisés selon le principe de séparation des responsabilités.

```
┌─────────────────────────────────────────────────────┐
│                   ORCHESTRATEUR                      │
│         (délégation, coordination, boucle)           │
└───────┬───────────┬────────────┬────────────────────┘
        │           │            │            │
   ┌────▼───┐  ┌────▼────┐ ┌────▼────┐ ┌────▼──────┐
   │Classify│  │Cryptana │ │Linguist │ │Pedagogue  │
   │  -er   │  │  -lyst  │ │         │ │           │
   └────────┘  └─────────┘ └─────────┘ └───────────┘
```

### 2.1 Rôle des agents

**Classifier** : Analyse les propriétés statistiques du texte chiffré (indice de coïncidence, fréquences de lettres, longueur) pour émettre une hypothèse sur la méthode de chiffrement utilisée.

**Cryptanalyst** : Applique les attaques adaptées à l'hypothèse du Classifier (force brute pour César, Kasiski + IC pour Vigenère, analyse fréquentielle pour substitution).

**Linguist** : Évalue la plausibilité linguistique des textes décryptés en calculant le taux de mots français reconnus dans le texte clair candidat.

**Pedagogue** : Produit une explication structurée du processus de déchiffrement, à destination de l'utilisateur final.

### 2.2 Boucle de correction

L'orchestrateur implémente une boucle de rétroaction : si le score linguistique retourné par l'agent Linguist est inférieur à un seuil (0.3), l'orchestrateur relance l'agent Cryptanalyst avec une hypothèse alternative.

---

## 3. Outils cryptographiques implémentés

### 3.1 Chiffrement de César

Substitution monoalphabétique par décalage fixe.

**Formule** : `C = (P + k) mod 26`

**Implémentation** : `scripts/chiffrement_cesar.py`

### 3.2 Chiffrement affine

Généralisation du César avec deux paramètres `(a, b)`. La contrainte `pgcd(a, 26) = 1` garantit la bijectivité.

**Formule** : `C = (a·P + b) mod 26`  
**Déchiffrement** : `P = a⁻¹·(C - b) mod 26`

### 3.3 Chiffrement de Vigenère

Chiffrement polyalphabétique utilisant une clé répétée. Résistant à la simple analyse de fréquences, mais vulnérable à l'analyse de Kasiski.

**Formule** : `C_i = (P_i + K_{i mod len(K)}) mod 26`

### 3.4 Chiffrement autoclave

Variante du Vigenère où la clé est étendue avec le texte clair lui-même. Plus résistant au Kasiski car la clé ne se répète pas de façon périodique régulière.

**Couverture de tests : 100 %**

### 3.5 Chiffrement par substitution

Chaque lettre est remplacée par une lettre unique selon une table fixe. L'espace des clés est 26! ≈ 4×10²⁶.

### 3.6 Chiffrement par transposition

Réarrangement des caractères selon une permutation des colonnes d'une grille.

**Couverture de tests : 97 %**

---

## 4. Corpus et données

### 4.1 Génération

Le corpus est généré par `scripts/generer_corpus.py` :

- **150 textes** en français, répartis entre les 6 méthodes.
- **3 longueurs** : courts (< 50 car.), moyens (50–200 car.), longs (> 200 car.).
- **Clés variées** : chaque méthode testée avec plusieurs clés distinctes.

### 4.2 Intégrité

Tous les fichiers sont référencés dans `SHA256SUMS` pour garantir leur intégrité.

---

## 5. Méthodes d'attaque cryptanalytique

### 5.1 Force brute (César)

Les 25 décalages possibles sont testés exhaustivement. Complexité : O(25·n).  
**Résultat** : Précision de 100 % sur le corpus (3 répétitions).

### 5.2 Analyse de Kasiski (Vigenère)

Recherche de séquences répétées. Les distances entre répétitions donnent via PGCD la longueur probable de la clé.

**Résultat** : Efficace pour des clés de 2 à 6 caractères sur textes > 100 caractères.

### 5.3 Indice de coïncidence

- Texte français naturel : IC ≈ 0.074
- Texte chiffré monoalphabétique : IC ≈ 0.065
- Texte chiffré polyalphabétique : IC ≈ 0.038–0.045

Permet de distinguer rapidement les types de chiffrement.

### 5.4 Test du chi-deux (χ²)

Compare la distribution des fréquences du texte chiffré avec celles du français pour chaque décalage possible.

### 5.5 Analyse fréquentielle

Comparaison des fréquences de lettres avec celles du français (E=14.7%, A=7.6%, S=7.9%…).

### 5.6 Score de quadgrammes

Évaluation de la qualité d'un texte clair par la probabilité des suites de 4 lettres selon un modèle appris sur le corpus français.

---

## 6. Expérimentations et résultats

Toutes les expériences ont été réalisées en **3 répétitions**. Résultats consignés dans `metrics.json`.

### 6.1 Précision force brute César

| Répétition | Précision |
|---|---|
| 1 | 100 % |
| 2 | 100 % |
| 3 | 100 % |
| **Moyenne** | **100 %** |

### 6.2 Indice de coïncidence par méthode

| Méthode | IC moyen | Interprétation |
|---|---|---|
| César | 0.0648 | Monoalphabétique → IC élevé |
| Affine | 0.0646 | Monoalphabétique → IC élevé |
| Vigenère (clé 6) | 0.0452 | Polyalphabétique → IC bas |
| Autoclave | 0.0401 | Plus aléatoire → IC très bas |

### 6.3 Robustesse Kasiski

| Clé | Longueur | Précision |
|---|---|---|
| AB | 2 | 85 % |
| CLE | 3 | 90 % |
| SECRET | 6 | 75 % |
| CRYPTO | 6 | 72 % |
| VIGENERE | 8 | 60 % |

La précision diminue avec la longueur de la clé.

### 6.4 Distance d'unicité

Pour une clé Vigenère de 6 lettres aléatoires, la distance d'unicité théorique est d'environ 25 caractères — confirmant que les textes courts restent difficiles à attaquer.

### 6.5 Couverture de tests

| Métrique | Valeur |
|---|---|
| Tests totaux | 95 |
| Couverture globale | 82 % |
| Module à 100 % | `chiffrement_autoclave` |
| Modules > 95 % | `entrainer_quadgrammes` (98 %), `telecharger_corpus` (98 %), `chiffrement_transposition` (97 %) |

---

## 7. Analyse de sécurité (STRIDE)

| Menace | Vecteur | Mitigation |
|---|---|---|
| Spoofing | Usurpation d'agent par injection | Agents isolés |
| Tampering | Modification du corpus | SHA256SUMS |
| Repudiation | Absence de logs | Logging structuré (à implémenter) |
| Information Disclosure | Fuite via logs | Logs sans contenu en clair |
| Denial of Service | Texte très long → timeout | Limite de taille sur les entrées |
| Elevation of Privilege | Non applicable | — |

---

## 8. Tests et qualité

### 8.1 Stratégie de test

- **Tests fonctionnels** : chiffrement puis déchiffrement retourne le message original.
- **Tests d'erreur** : entrées invalides lèvent des `ValueError` explicites.
- **Tests d'attaque** : les fonctions retrouvent la clé correcte sur des cas connus.

### 8.2 Pipeline CI/CD

GitHub Actions exécute les 95 tests à chaque `push` et `pull_request` sur `main`, avec mesure de couverture via `pytest-cov`.

---

## 9. Limitations et travaux futurs

### Limitations

- Vocabulaire de l'agent Linguist limité à 34 mots.
- Kasiski peu fiable sur textes courts ou clés > 8 caractères.
- Pas de gestion des caractères accentués (textes normalisés en ASCII majuscules).

### Pistes d'amélioration

- Modèle de langue complet (bigrammes, trigrammes).
- Attaque hill climbing pour la substitution.
- Interface web de démonstration.
- Extension à d'autres langues.

---

## 10. Conclusion

Vigenere-Squad démontre qu'une architecture multi-agents modulaire permet d'organiser efficacement la complexité d'un système de cryptanalyse. Les six chiffrements classiques sont correctement implémentés et testés (95 tests, 82 % de couverture). Les attaques couvrent les principales techniques de la cryptanalyse classique, et les expériences confirment les propriétés théoriques des chiffrements.

Le projet est prêt pour une release v1.0.0.

---

*Rapport généré le 2026-11-19 — Équipe Vigenere-Squad*