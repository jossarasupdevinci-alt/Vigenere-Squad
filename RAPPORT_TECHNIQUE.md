# RAPPORT TECHNIQUE — VIGENERE-SQUAD

**Version du projet :** 0.1.0  
**Date de mise à jour :** 21 novembre 2026  
**Langage :** Python 3.12.3  
**Dépôt :** https://github.com/jossarasupdevinci-alt/Vigenere-Squad

---

## 1. Présentation du projet

Vigenere-Squad est un projet Python de cryptanalyse classique reposant sur une architecture multi-agents.

Son objectif est d'analyser différents chiffrements classiques, d'identifier des méthodes et des clés possibles, de rechercher des solutions de déchiffrement et de présenter les résultats de manière pédagogique.

Le projet associe des outils cryptographiques déterministes, des analyses statistiques et une collaboration entre agents spécialisés.

Il vise également à évaluer les performances, la fiabilité et les limites des techniques de cryptanalyse, notamment lorsque les messages sont courts ou que les méthodes de chiffrement ne présentent pas de périodicité exploitable.

## 2. Objectifs du projet

Les principaux objectifs sont :

- Identifier les méthodes de chiffrement classiques.
- Analyser les textes chiffrés.
- Détecter des clés possibles.
- Mettre en œuvre des techniques de cryptanalyse adaptées à chaque méthode.
- Déchiffrer les messages lorsque les informations disponibles le permettent.
- Expliquer les résultats de manière pédagogique.
- Évaluer les performances et les limites des méthodes de cryptanalyse.
- Comparer les résultats obtenus avec et sans assistance d'agents intelligents.

## 3. Architecture du système

Le projet est organisé autour d'une architecture multi-agents coordonnée par un orchestrateur.

Les agents spécialisés sont :

- **Classifier :** identification des méthodes de chiffrement probables.
- **Cryptanalyst :** analyses statistiques et cryptanalytiques, recherche de clés et génération de candidats de déchiffrement.
- **Linguist :** évaluation de la cohérence linguistique des textes obtenus.
- **Pedagogue :** explication des méthodes et des résultats.

L'orchestrateur coordonne les interventions des agents et centralise les résultats.

L'approche repose sur une séparation entre les calculs cryptographiques déterministes et l'interprétation des résultats. Les outils Python effectuent les opérations vérifiables, tandis que les agents contribuent à l'analyse et à la présentation des conclusions.

## 4. Méthodes de chiffrement étudiées

Le projet couvre six familles de chiffrements classiques :

1. César.
2. Affine.
3. Vigenère.
4. Autokey (Autoclave).
5. Substitution monoalphabétique.
6. Transposition.

Ces méthodes permettent d'étudier différentes propriétés cryptographiques : décalage, substitution, périodicité, dépendance du texte clair et réorganisation des caractères.

## 5. Techniques d'analyse et de cryptanalyse

Les techniques étudiées et intégrées comprennent :

- **Indice de coïncidence :** mesure de la distribution statistique des lettres.
- **Analyse fréquentielle :** comparaison des fréquences observées avec les fréquences linguistiques.
- **Test du chi-deux :** évaluation de la proximité entre une distribution de lettres et une distribution de référence.
- **Méthode de Kasiski :** recherche de séquences répétées et analyse des distances entre leurs occurrences.
- **Analyse de Friedman :** estimation de propriétés liées à la longueur de clé.
- **Scores linguistiques et quadgrammes :** évaluation de la vraisemblance linguistique des textes candidats.
- **Recherche par force brute :** exploration des clés possibles lorsque leur espace de recherche est suffisamment limité.
- **Recuit simulé :** recherche heuristique d'une clé de substitution monoalphabétique.

## 6. Développements réalisés

### 6.1. Chiffrement et déchiffrement

Des modules Python ont été développés pour les six familles de chiffrements étudiées.

Les fonctions de chiffrement et de déchiffrement sont accompagnées de tests automatisés permettant notamment de vérifier les opérations inverses, la validation des clés et le traitement des caractères non alphabétiques.

### 6.2. Attaque par substitution monoalphabétique

Une attaque fondée sur le recuit simulé a été développée dans `scripts/attaque_substitution.py`.

La méthode repose sur les étapes suivantes :

1. Génération d'une clé de substitution initiale.
2. Production d'une clé voisine par permutation de lettres.
3. Déchiffrement du texte avec la clé candidate.
4. Évaluation du texte à partir d'un score linguistique basé sur les quadgrammes.
5. Acceptation ou rejet de la nouvelle clé selon la stratégie du recuit simulé.
6. Conservation de la meilleure solution trouvée.

Un essai expérimental réalisé sur un texte français de 1 000 lettres a permis de retrouver la clé utilisée et de reconstituer le texte clair avec une précision de 100 %.

La configuration testée utilisait 100 000 itérations.

L'attaque a également été intégrée dans l'agent Cryptanalyst. Son résultat est comparé aux autres candidats de cryptanalyse et sa sélection est conditionnée par une longueur minimale de texte de 500 caractères.

Des tests spécifiques et un test d'intégration ont été réalisés.

### 6.3. Étude du chiffrement Autokey et des limites de Kasiski

Une étude expérimentale a été menée pour comprendre pourquoi la méthode de Kasiski n'est pas directement adaptée au chiffrement Autokey.

Dans Vigenère classique, la clé est répétée périodiquement. Dans la variante Autokey implémentée dans le projet, les lettres du texte clair prolongent la clé initiale. Le flux de clé devient donc dépendant du message et ne conserve pas la périodicité du Vigenère classique.

La méthode de Kasiski recherche des répétitions et exploite les distances entre leurs occurrences. Son hypothèse de périodicité devient donc inadaptée à cette variante d'Autokey.

#### Protocole expérimental

Une première comparaison a été réalisée avec une clé de trois caractères (`CLE`), puis avec une clé de six caractères (`SOLEIL`).

Les textes provenaient du corpus français `data/corpus_francais.txt`.

Une seconde expérience a comparé les deux méthodes sur dix clés générées avec une graine aléatoire fixe de 42.

Les longueurs de texte testées étaient :

- 100 caractères ;
- 200 caractères ;
- 300 caractères ;
- 400 caractères.

L'indicateur mesuré était le taux de détection exacte de la longueur de clé par Kasiski.

#### Résultats obtenus

| Longueur du texte | Vigenère | Autokey |
|---:|---:|---:|
| 100 caractères | 30 % | 0 % |
| 200 caractères | 20 % | 0 % |
| 300 caractères | 20 % | 0 % |
| 400 caractères | 20 % | 0 % |

Ces résultats montrent que, dans les conditions de cette expérience, Kasiski retrouve parfois la longueur de clé pour Vigenère classique, mais ne la retrouve dans aucun des essais Autokey.

Ils mettent également en évidence une limite de l'implémentation actuelle de Kasiski : les répétitions accidentelles peuvent perturber le calcul du PGCD, y compris pour Vigenère classique.

Ces résultats sont donc propres au protocole testé et ne constituent pas une preuve universelle de l'échec de Kasiski sur tous les textes Vigenère.

**État du développement :** le chiffrement et le déchiffrement Autokey sont implémentés et testés. L'étude comparative de Kasiski est réalisée. La conception et l'implémentation d'une attaque spécifique à Autokey restent à effectuer.

## 7. Génération du corpus expérimental

Le projet dispose d'un corpus français de référence situé dans `data/corpus_francais.txt`.

Un générateur de corpus a été développé dans `scripts/generer_corpus.py`.

Il permet de produire des messages chiffrés selon les six méthodes étudiées.

La configuration prévue par défaut comprend :

- 150 messages chiffrés ;
- six méthodes de chiffrement ;
- des longueurs comprises entre 80 et 2 000 caractères ;
- des clés de longueur comprise entre 3 et 12 caractères ;
- une graine aléatoire fixée à 42 pour favoriser la reproductibilité.

Les messages générés sont enregistrés dans `data/corpus_genere/messages`.

Les références privées contenant les informations nécessaires à l'évaluation sont conservées séparément. Elles ne doivent pas être publiées avec les données chiffrées destinées aux expériences.

## 8. Technologies et environnement

Les technologies et outils utilisés comprennent :

| Technologie | Utilisation |
|---|---|
| Python 3.12.3 | Développement |
| Visual Studio Code | Environnement de développement |
| Git | Gestion des versions |
| GitHub | Hébergement du dépôt |
| pytest | Tests automatisés |
| pytest-cov | Mesure de couverture |
| Quadgrammes français | Évaluation linguistique |
| Architecture multi-agents | Coordination des analyses |

## 9. Organisation du dépôt

| Répertoire ou fichier | Fonction |
|---|---|
| `agents/` | Agents spécialisés et orchestrateur |
| `scripts/` | Outils de chiffrement, de déchiffrement et de cryptanalyse |
| `tests/` | Tests automatisés |
| `data/` | Corpus et données de référence |
| `docs/` | Documentation complémentaire |
| `logs/` | Traces d'exécution |
| `AI_USAGE.md` | Documentation de l'utilisation de l'IA |
| `AUDIT.md` | Vérifications et audit du projet |
| `SYSTEM_CARD.md` | Présentation du système et de ses limites |
| `metrics.json` | Mesures et résultats structurés |
| `RAPPORT_TECHNIQUE.md` | Présent rapport |

## 10. Vérification et tests automatisés

Une exécution de la suite de tests automatisés réalisée le 20 novembre 2026 a produit les résultats suivants :

| Indicateur | Résultat |
|---|---:|
| Tests réussis | 119 |
| Tests échoués | 0 |
| Avertissements | 1 |
| Durée d'exécution | 94,17 secondes |
| Couverture globale rapportée | 83 % |

Un avertissement Python concerne l'exécution directe du module `agents.orchestrator` après son chargement préalable.

Les tests spécifiques à l'attaque par substitution et les tests des agents ont également été exécutés :

- 24 tests réussis ;
- 0 échec ;
- 1 avertissement ;
- durée : 13,07 secondes.

Ces résultats attestent du passage des suites de tests exécutées. Ils ne constituent pas à eux seuls une validation exhaustive de toutes les fonctionnalités du système.

## 11. Sécurité, robustesse et limites

Vigenere-Squad est un projet pédagogique et expérimental.

Les chiffrements classiques étudiés ne constituent pas des mécanismes de sécurité adaptés aux usages cryptographiques modernes.

Plusieurs facteurs peuvent influencer les résultats :

- la longueur du texte chiffré ;
- la longueur et la nature de la clé ;
- la langue du texte ;
- la présence d'espaces et de ponctuation ;
- les erreurs introduites dans le texte ;
- la qualité du corpus linguistique ;
- les limites des méthodes statistiques et heuristiques.

Les entrées et les résultats des agents doivent être contrôlés. Les conclusions produites ne doivent pas être considérées comme systématiquement exactes.

La robustesse face aux textes sans espaces, aux erreurs introduites et aux textes anglais doit faire l'objet d'expériences complémentaires.

## 12. Évaluation expérimentale et travaux restants

L'évaluation du projet doit permettre d'étudier les performances des méthodes de cryptanalyse, leur robustesse et leurs limites.

Les travaux déjà réalisés comprennent :

- le développement des chiffrements classiques ;
- la mise en place des tests automatisés ;
- l'attaque par recuit simulé de la substitution monoalphabétique ;
- l'intégration de cette attaque dans l'agent Cryptanalyst ;
- la comparaison expérimentale entre Vigenère et Autokey face à Kasiski ;
- la mesure de la couverture globale des tests.

Les travaux restant à approfondir comprennent :

- la conception et l'implémentation d'une attaque dédiée à Autokey ;
- l'étude de la distance d'unicité de Shannon et de la longueur minimale de texte nécessaire à une attaque réussie ;
- l'évaluation sur plusieurs répétitions expérimentales ;
- les tests de robustesse ;
- la comparaison des configurations avec et sans assistance d'agents ;
- l'évaluation des performances globales du système multi-agents ;
- la consolidation des résultats dans `metrics.json`.

Les résultats expérimentaux doivent être reproductibles et accompagnés de leur protocole, de leurs paramètres et de leurs limites.

## 13. Conclusion

Vigenere-Squad propose une approche pédagogique de la cryptanalyse classique fondée sur une architecture multi-agents.

Le projet associe des outils déterministes, des analyses statistiques, des méthodes heuristiques et une interprétation linguistique des résultats.

Les travaux réalisés ont permis de développer les six familles de chiffrements étudiées, de mettre en place une suite de tests automatisés et d'intégrer une attaque par recuit simulé contre la substitution monoalphabétique.

Une première étude expérimentale a également mis en évidence les limites de Kasiski face au chiffrement Autokey.

Le projet dispose ainsi d'une base technique et expérimentale. Les prochaines étapes portent notamment sur l'attaque spécifique d'Autokey, l'étude de la distance d'unicité, les tests de robustesse et l'évaluation approfondie de l'architecture multi-agents.
