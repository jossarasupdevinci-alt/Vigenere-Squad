# Rapport Technique — Vigenere-Squad

**Version** : 1.0.0
**Date** : 2026-11-19

## 1. Introduction

Vigenere-Squad est un système multi-agents de cryptanalyse classique.
Il implémente six méthodes de chiffrement sur un corpus de 150 textes français.

## 2. Architecture

Orchestrateur central coordonnant 4 agents :
- Classifier : identifie la méthode de chiffrement
- Cryptanalyst : mène les attaques
- Linguist : évalue la plausibilité linguistique
- Pedagogue : explique les résultats

Boucle de correction : si score linguistique < 0.3, relance avec hypothèse alternative.

## 3. Chiffrements

- César : C = (P + k) mod 26
- Affine : C = (a*P + b) mod 26, avec pgcd(a,26)=1
- Vigenère : Ci = (Pi + K[i mod len(K)]) mod 26
- Autoclave : clé étendue avec le texte clair
- Substitution : permutation fixe de l'alphabet (26! clés possibles)
- Transposition : réarrangement par colonnes

## 4. Corpus

150 textes français, 3 longueurs (courts, moyens, longs), 6 méthodes.
Fichiers vérifiés par SHA256SUMS.

## 5. Attaques

- Force brute César : 25 décalages testés, précision 100 %
- Kasiski : détection longueur clé Vigenère par PGCD des répétitions
- Indice de coïncidence : IC ≈ 0.065 (mono) vs 0.040 (poly)
- Chi-deux : compare fréquences du texte vs français
- Analyse fréquentielle : E=14.7%, A=7.6%, S=7.9%
- Quadgrammes : score de probabilité sur suites de 4 lettres

## 6. Expériences (3 répétitions)

| Expérience | Résultat |
|---|---|
| Force brute César | 100 % précision |
| IC César | 0.0648 |
| IC Vigenère | 0.0452 |
| Kasiski clé 3 | 90 % |
| Kasiski clé 8 | 60 % |
| Couverture tests | 82 % |

## 7. Sécurité STRIDE

Voir SYSTEM_CARD.md pour l'analyse complète.
Risques principaux : injection de prompt, corpus empoisonné, faux positifs classifier.

## 8. Tests

95 tests automatisés, 82 % de couverture globale.
CI/CD via GitHub Actions avec pytest-cov.

## 9. Limitations

- Kasiski peu fiable sur textes courts ou clés > 8 caractères.
- Vocabulaire Linguist limité à 34 mots.
- Pas de support des caractères accentués.

## 10. Conclusion

Architecture multi-agents modulaire efficace pour la cryptanalyse classique.
95 tests passent, corpus complet, expériences en 3 répétitions.
Prêt pour release v1.0.0.
