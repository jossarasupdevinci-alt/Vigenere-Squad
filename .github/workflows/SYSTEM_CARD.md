# SYSTEM CARD â€” Vigenere-Squad

## 1. PrÃ©sentation du systÃ¨me

**Nom :** Vigenere-Squad
**Type :** SystÃ¨me multi-agents de cryptanalyse classique
**Domaine :** Cryptographie et sÃ©curitÃ© de l'information

Vigenere-Squad est un projet Python visant Ã  analyser et Ã  Ã©tudier diffÃ©rents chiffrements classiques Ã  travers une architecture multi-agents coordonnÃ©e par un orchestrateur.

## 2. Objectifs

- Identifier des mÃ©thodes de chiffrement classiques.
- Analyser les caractÃ©ristiques statistiques des textes chiffrÃ©s.
- Proposer des pistes de cryptanalyse.
- Ã‰valuer la plausibilitÃ© linguistique des textes dÃ©chiffrÃ©s.
- Expliquer les rÃ©sultats obtenus.

## 3. Architecture multi-agents

Le systÃ¨me repose sur un orchestrateur et plusieurs agents spÃ©cialisÃ©s :

- **Classifier :** identifie la mÃ©thode de chiffrement probable.
- **Cryptanalyst :** rÃ©alise les analyses et les attaques cryptanalytiques.
- **Linguist :** Ã©value la cohÃ©rence linguistique des rÃ©sultats.
- **Pedagogue :** explique les mÃ©thodes et les rÃ©sultats Ã  l'utilisateur.

## 4. MÃ©thodes de chiffrement Ã©tudiÃ©es

Le projet couvre six familles de chiffrements classiques :

1. CÃ©sar
2. Affine
3. VigenÃ¨re
4. Autoclave
5. Substitution monoalphabÃ©tique
6. Transposition

## 5. MÃ©thodes d'analyse

Les techniques Ã©tudiÃ©es comprennent notamment :

- L'indice de coÃ¯ncidence.
- L'analyse frÃ©quentielle.
- Le test du chi-deux.
- La mÃ©thode de Kasiski.
- L'analyse de Friedman.
- Le calcul de scores linguistiques et de quadgrammes.
- Les recherches par force brute lorsque cela est applicable.

## 6. SÃ©curitÃ© et limites

Les rÃ©sultats produits dÃ©pendent de la longueur des messages, de la mÃ©thode de chiffrement, de la qualitÃ© du texte et des hypothÃ¨ses utilisÃ©es.

Les chiffrements classiques Ã©tudiÃ©s ne reprÃ©sentent pas des mÃ©canismes de sÃ©curitÃ© modernes.

Les sorties des agents doivent Ãªtre vÃ©rifiÃ©es et ne doivent pas Ãªtre considÃ©rÃ©es comme systÃ©matiquement exactes.

## 7. Ã‰valuation

L'Ã©valuation du systÃ¨me repose sur :

- Des tests automatisÃ©s.
- La vÃ©rification des fonctions cryptographiques.
- L'analyse des performances des mÃ©thodes de cryptanalyse.
- L'Ã©tude de la robustesse face aux erreurs et aux entrÃ©es atypiques.
- La mesure de la couverture des tests.

Les rÃ©sultats quantitatifs dÃ©finitifs sont consignÃ©s dans `metrics.json` aprÃ¨s vÃ©rification expÃ©rimentale.

## 8. ResponsabilitÃ©

Vigenere-Squad est un projet pÃ©dagogique et expÃ©rimental. Il a pour objectif d'illustrer les principes de la cryptanalyse classique et le fonctionnement d'une architecture multi-agents.
