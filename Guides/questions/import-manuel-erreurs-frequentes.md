# Import manuel d’une ressource sur data.gouv : erreurs fréquentes (CSV, codes, SIRET)

Cette fiche recense les erreurs les plus courantes lors de l’import manuel d’une ressource (fichier) sur data.gouv.fr, et les bonnes pratiques associées.

## Sommaire

- [Préconisations et points de vigilance](#préconisations-et-points-de-vigilance)
- [Normalisation générale](#1-normalisation-générale)
- [Données géographiques](#2-données-géographiques)
- [SIRET](#3-siret-14-caractères)
- [SIREN](#4-siren-9-caractères)

## Préconisations et points de vigilance

### Top 10 des bonnes pratiques

- Utiliser le format **CSV**
- Éviter les **espaces et caractères spéciaux dans les noms de champs**
- Limiter les noms de champs à **63 caractères**
- Utiliser le **code commune INSEE** plutôt que le code postal
- Formater correctement **SIREN (9)** et **SIRET (14)** dans Excel
- Ne pas mélanger dans une même colonne SIREN et SIRET
- Ne pas utiliser **plusieurs feuilles** dans un même fichier
- Ne pas **fusionner les cellules ou les colonnes**
- Rappel : les **couleurs et mises en forme Excel ne sont pas prises en compte**
- Privilégier l'**alignement avec des référentiels et des vocabulaires**

## 1) Normalisation générale

### Privilégier le format CSV
- Utiliser **CSV** (format ouvert, non propriétaire).  
Sur la plateforme nationale des données ouvertes, ce format permet la génération des **prévisualisations** et **datavisualisations** automatisées (exemple : génération d'une carte lors de la présence de données de localisation).

### Nom des champs / variables

#### Nombre de caractères
Ne pas dépasser 63 caractères (au-delà, le fichier ne peut être analysé et aucune datavisualisation ne sera disponible).  
Il est recommandé d'accompagner le jeu de données d'un **fichier** de description des champs / variables **utilisés** dans les documents complémentaires.

#### Caractères spéciaux
Évitez les espaces, les majuscules et les caractères spéciaux (hors _ et -).  
Les caractères spéciaux **complexifient** l'**interopérabilité** et les réutilisations.

## 2) Données géographiques
- Pour les référencements territoriaux, s’appuyer sur le **Code officiel géographique (COG)** : https://www.insee.fr/fr/information/2560452  
Cette nomenclature de référence rassemble les codes et libellés, au 1er janvier de l’année en cours, des communes, cantons, arrondissements, départements, collectivités territoriales ayant les compétences départementales, régions et pays et territoires étrangers.

Exemples de variables :
- code_commune
- code_canton
- code_departement
- code_region
- code_arrondissement
- code_pays
- codes_communes_outre_mer

### 2.1) Code commune INSEE : privilégier le code commune INSEE (plutôt que le code postal)

- Utiliser le **code commune du Code officiel géographique (COG) publié par l’INSEE**, via `code_commune`
- Le **code postal** n’est pas recommandé : **un même code postal peut correspondre à plusieurs communes**.

#### Paramétrer le format sous Excel 
Dans Excel, définir le format de cellule : **Format de cellule** → **Spécial** → **Code postal**
Objectif : éviter la perte des zéros initiaux (ex. 06000 transformé en 6000).

### 2.2) Si le code postal est utilisé (non recommandé)
Le **code postal** n’est pas recommandé : **un même code postal peut correspondre à plusieurs communes** (et inversement).
#### Paramétrer le format sous Excel 
- Dans Excel, définir le format de cellule : **Format de cellule** → **Spécial** → **Code postal**
- Objectif : éviter la perte des **zéros initiaux** (ex. `06000` transformé en `6000`).

## 3) SIRET (14 caractères)
Référence : https://annuaire-entreprises.data.gouv.fr/definitions/numero-siret
- Dans Excel, définir le format de cellule :
  - **Format de cellule** → **Personnalisé**
  - Masque : `00000000000000` (14 zéros)
- Objectif : conserver les **14 chiffres** et les **zéros initiaux**.

## 4) SIREN (9 caractères)
Référence : https://annuaire-entreprises.data.gouv.fr/definitions/numero-siren
- Dans Excel, définir le format de cellule :
  - **Format de cellule** → **Personnalisé**
  - Masque : `000000000` (9 zéros)
- Objectif : conserver les **9 chiffres** et les **zéros initiaux**.
