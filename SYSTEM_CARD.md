# System Card — Vigenere-Squad

**Nom** : Vigenere-Squad
**Version** : 1.0.0
**Date** : 2026-11-19
**Type** : Système multi-agents de cryptanalyse classique

## Description

Orchestrateur central coordonnant 4 agents spécialisés :
- Classifier : identifie la méthode de chiffrement
- Cryptanalyst : mène les attaques cryptanalytiques
- Linguist : évalue la plausibilité linguistique
- Pedagogue : explique les résultats

## Capacités

| Capacité | Détail |
|---|---|
| Chiffrements | César, Affine, Vigenère, Autoclave, Substitution, Transposition |
| Attaques | Force brute, Kasiski, IC, fréquentiel, chi-deux |
| Corpus | 150 textes français |
| Tests | 95 tests, couverture 82 % |

## Limitations

- Kasiski nécessite des textes > 50 caractères.
- Vocabulaire Linguist limité à 34 mots.
- Pas de support des chiffrements modernes (AES, RSA).

## Analyse STRIDE

| Menace | Vecteur | Mitigation |
|---|---|---|
| Spoofing | Usurpation d'agent | Agents isolés |
| Tampering | Modification corpus | SHA256SUMS |
| Repudiation | Absence de logs | Logging à implémenter |
| Information Disclosure | Fuite via logs | Logs sans contenu clair |
| Denial of Service | Texte très long | Limite de taille |
| Elevation of Privilege | Non applicable | — |

## Usage prévu

Exclusivement académique et pédagogique.
