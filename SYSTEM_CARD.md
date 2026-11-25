# System Card — Vigenere-Squad

**Nom** : Vigenere-Squad
**Version** : 1.0.0
**Date** : 2026-11-19
**Type** : Système multi-agents de cryptanalyse classique

## Description

Vigenere-Squad est une plateforme multi-agents pour chiffrer, déchiffrer et attaquer des chiffrements classiques. Agents : Classifier, Cryptanalyst, Linguist, Pedagogue.

## Capacités

| Capacité | Détail |
|---|---|
| Chiffrements | César, Affine, Vigenère, Autoclave, Substitution, Transposition |
| Attaques | Force brute, Kasiski, IC, analyse fréquentielle, chi-deux |
| Corpus | 150 textes français, 6 méthodes |
| Tests | 95 tests, couverture 82% |

## Limitations

- Kasiski nécessite des textes > 50 caractères.
- Vocabulaire linguistique limité à 34 mots.
- Clés > 8 caractères réduisent la précision de Kasiski.
- Non conçu pour les chiffrements modernes (AES, RSA).

## Analyse STRIDE

| Menace | Vecteur | Mitigation |
|---|---|---|
| Spoofing | Usurpation d'agent par injection | Agents isolés |
| Tampering | Modification du corpus | SHA256SUMS |
| Repudiation | Absence de logs | Logging structuré à implémenter |
| Information Disclosure | Fuite via logs | Logs sans contenu en clair |
| Denial of Service | Texte très long | Limite de taille sur les entrées |
| Elevation of Privilege | Non applicable | — |

## Injections de prompt

Les entrées sont traitées comme données statistiques opaques, jamais comme instructions.

## Données empoisonnées

Corpus généré localement par generer_corpus.py. Fichiers vérifiés par SHA256SUMS.

## Usage prévu

Cadre exclusivement académique et pédagogique — Promotion 2026.
