# RAPPORT TECHNIQUE — VIGENERE-SQUAD

**Version du projet :** 0.1.0
**Date :** 20 novembre 2026

## 1. Présentation du projet

Vigenere-Squad est un projet Python de cryptanalyse classique reposant sur une architecture multi-agents.

Son objectif est d'analyser différents chiffrements classiques, d'identifier des méthodes et des clés possibles, de rechercher des solutions de déchiffrement et de présenter les résultats de manière pédagogique.

Le projet associe des outils cryptographiques déterministes et une collaboration entre agents spécialisés.

## 2. Objectifs

Les principaux objectifs sont :

- Identifier les méthodes de chiffrement.
- Analyser les textes chiffrés.
- Détecter des clés possibles.
- Déchiffrer les messages.
- Expliquer les résultats de manière pédagogique.
- Évaluer les capacités et les limites des méthodes de cryptanalyse.

## 3. Architecture du système

Le projet est organisé autour d'une architecture multi-agents coordonnée par un orchestrateur.

Les agents spécialisés sont :

- **Classifier :** identification des méthodes de chiffrement probables.
- **Cryptanalyst :** analyses statistiques et cryptanalytiques.
- **Linguist :** évaluation de la cohérence linguistique.
- **Pedagogue :** explication des méthodes et des résultats.

L'approche repose sur la séparation entre les calculs cryptographiques déterministes et l'interprétation des résultats.

## 4. Méthodes de chiffrement étudiées

Le projet couvre six familles de chiffrements classiques :

1. César.
2. Affine.
3. Vigenère.
4. Autoclave.
5. Substitution monoalphabétique.
6. Transposition.

## 5. Techniques d'analyse

Les techniques étudiées comprennent :

- Indice de coïncidence.
- Analyse fréquentielle.
- Test du chi-deux.
- Méthode de Kasiski.
- Analyse de Friedman.
- Scores linguistiques et quadgrammes.
- Recherche par force brute lorsque cela est applicable.

## 6. Technologies et environnement

- Langage : Python.
- Environnement de développement : Visual Studio Code.
- Gestion de versions : Git et GitHub.
- Tests automatisés : pytest.
- Domaine : cryptographie classique et intelligence artificielle.

## 7. Organisation du dépôt

| Répertoire | Fonction |
|---|---|
| `agents/` | Agents spécialisés |
| `scripts/` | Outils et programmes Python |
| `tests/` | Tests automatisés |
| `data/` | Jeux de données |
| `docs/` | Documentation |
| `logs/` | Traces d'exécution |

## 8. Vérification et tests

Une exécution de la suite de tests automatisés réalisée le 20 novembre 2026 a produit les résultats suivants :

- Tests réussis : 119.
- Tests échoués : 0.
- Avertissements : 1.
- Durée d'exécution : 94,17 secondes.

Un avertissement Python concerne l'exécution directe du module `agents.orchestrator` après son chargement préalable.

Ces résultats attestent du passage de la suite de tests exécutée, mais ne constituent pas à eux seuls une validation exhaustive de toutes les fonctionnalités du système.

## 9. Sécurité et limites

Vigenere-Squad est un projet pédagogique et expérimental.

Les chiffrements classiques étudiés ne constituent pas des mécanismes de sécurité adaptés aux usages cryptographiques modernes.

Les résultats peuvent varier selon la longueur des messages, la méthode utilisée, la qualité linguistique et les caractéristiques des clés.

Les entrées et les résultats des agents doivent être contrôlés. Les conclusions produites ne doivent pas être considérées comme systématiquement exactes.

## 10. Évaluation expérimentale

L'évaluation doit permettre d'étudier les performances des méthodes de cryptanalyse, leur robustesse et leurs limites.

Les résultats quantitatifs définitifs doivent être obtenus à partir d'expériences reproductibles et consignés dans `metrics.json`.

Aucune métrique expérimentale non vérifiée n'est déclarée dans ce rapport.

## 11. Conclusion

Vigenere-Squad propose une approche pédagogique de la cryptanalyse classique fondée sur une architecture multi-agents.

Le projet met en relation l'analyse statistique, les techniques de déchiffrement et l'explication des résultats.

Les tests automatisés constituent une première étape de validation. Des vérifications complémentaires des expériences, de la robustesse et de la sécurité restent nécessaires pour établir une évaluation complète du système.
