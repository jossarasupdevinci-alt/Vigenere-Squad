# SYSTEM CARD — Vigenere-Squad

## 1. Présentation du système

**Nom :** Vigenere-Squad
**Type :** Système multi-agents de cryptanalyse classique
**Domaine :** Cryptographie et sécurité de l'information

Vigenere-Squad est un projet Python visant à analyser et à étudier différents chiffrements classiques à travers une architecture multi-agents coordonnée par un orchestrateur.

## 2. Objectifs

- Identifier des méthodes de chiffrement classiques.
- Analyser les caractéristiques statistiques des textes chiffrés.
- Proposer des pistes de cryptanalyse.
- Évaluer la plausibilité linguistique des textes déchiffrés.
- Expliquer les résultats obtenus.

## 3. Architecture multi-agents

Le système repose sur un orchestrateur et plusieurs agents spécialisés :

- **Classifier :** identifie la méthode de chiffrement probable.
- **Cryptanalyst :** réalise les analyses et les attaques cryptanalytiques.
- **Linguist :** évalue la cohérence linguistique des résultats.
- **Pedagogue :** explique les méthodes et les résultats à l'utilisateur.

## 4. Méthodes de chiffrement étudiées

Le projet couvre six familles de chiffrements classiques :

1. César
2. Affine
3. Vigenère
4. Autoclave
5. Substitution monoalphabétique
6. Transposition

## 5. Méthodes d'analyse

Les techniques étudiées comprennent notamment :

- L'indice de coïncidence.
- L'analyse fréquentielle.
- Le test du chi-deux.
- La méthode de Kasiski.
- L'analyse de Friedman.
- Le calcul de scores linguistiques et de quadgrammes.
- Les recherches par force brute lorsque cela est applicable.

## 6. Sécurité et limites

Les résultats produits dépendent de la longueur des messages, de la méthode de chiffrement, de la qualité du texte et des hypothèses utilisées.

Les chiffrements classiques étudiés ne représentent pas des mécanismes de sécurité modernes.

Les sorties des agents doivent être vérifiées et ne doivent pas être considérées comme systématiquement exactes.

## 7. Évaluation

L'évaluation du système repose sur :

- Des tests automatisés.
- La vérification des fonctions cryptographiques.
- L'analyse des performances des méthodes de cryptanalyse.
- L'étude de la robustesse face aux erreurs et aux entrées atypiques.
- La mesure de la couverture des tests.

Les résultats quantitatifs définitifs sont consignés dans `metrics.json` après vérification expérimentale.

## 8. Responsabilité

Vigenere-Squad est un projet pédagogique et expérimental. Il a pour objectif d'illustrer les principes de la cryptanalyse classique et le fonctionnement d'une architecture multi-agents.