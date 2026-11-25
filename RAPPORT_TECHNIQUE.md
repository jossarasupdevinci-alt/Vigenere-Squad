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

## 3. Chiffrements

- César : C = (P + k) mod 26
- Affine : C = (a*P + b) mod 26
- Vigenère : Ci = (Pi + K[i mod len(K)]) mod 26
- Autoclave : clé étendue avec le texte clair
- Substitution : permutation fixe de l'alphabet
- Transposition : réarrangement par colonnes
