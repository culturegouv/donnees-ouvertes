# Guide de bonnes pratiques pour formater une ressource avant son import sur data.gouv.fr

Cette fiche présente les bonnes pratiques à respecter lors du formatage et de l'import manuel d'une ressource (fichier) sur data.gouv.fr.\
Elle vise à faciliter l'exploitation des données sur la plateforme, notamment la génération des **prévisualisations** et des **datavisualisations automatiques**.

------------------------------------------------------------------------

## Sommaire

- [Bonnes pratiques de formatage](#bonnes-pratiques-de-formatage)
- [Vérifications avant et après l'import](#vérifications-avant-et-après-limport)
- [Erreurs fréquemment rencontrées](#erreurs-fréquemment-rencontrées)
- [Normalisation générale](#normalisation-générale)
- [Données géographiques](#données-géographiques)
- [SIRET](#siret-14-caractères)
- [SIREN](#siren-9-caractères)
- [Valeurs nulles et zéros](#valeurs-nulles-et-zéros)

------------------------------------------------------------------------

# Bonnes pratiques de formatage

### Principes généraux

-   Utiliser le format **CSV**
-   Utiliser des **noms de champs simples**, sans espaces ni caractères
    spéciaux
-   Limiter les noms de champs à **63 caractères**
-   Utiliser le **code commune INSEE** pour les référencements
    territoriaux
-   Utiliser des colonnes distinctes pour les **identifiants
    d'entreprises** (`SIREN`, `SIRET`)
-   Utiliser **une seule feuille par fichier**
-   Utiliser une **structure tabulaire simple**, sans cellules
    fusionnées
-   Se rappeler que les **couleurs et mises en forme Excel ne sont pas
    prises en compte**
-   Privilégier l'**alignement avec des référentiels et vocabulaires**
-   Structurer les données selon le principe : **une colonne = une
    information**

Exemples :

  Mauvaise pratique                         Bonne pratique
  ----------------------------------------- --------------------------
  SIREN et SIRET dans la même colonne       deux colonnes distinctes
  code commune et code outre-mer mélangés   deux colonnes distinctes

------------------------------------------------------------------------

# Vérifications avant et après l'import

Certaines transformations automatiques peuvent être appliquées par les tableurs (Excel, LibreOffice, etc.) lors de la préparation ou de l'export d'un fichier.\
Il est recommandé de vérifier certains champs **avant l'export au format CSV** et **après l'import sur data.gouv.fr**.

------------------------------------------------------------------------

## Vérifications avant l'import

Avant d'exporter le fichier en CSV, vérifier en priorité :

**Codes géographiques**

Vérifier que les **zéros initiaux sont conservés**.

Exemple :

    06088 → 6088

**Identifiants d'entreprises**

Vérifier que les **SIREN et SIRET ne sont pas affichés en notation scientifique**.

Exemple :

    55210055400013 → 5,52101E+13

**Pourcentages**

Vérifier qu'aucune conversion automatique n'a été appliquée.

Exemple :

    2 % → 0,02

**Dates**

Vérifier que certaines valeurs n'ont pas été **interprétées automatiquement comme des dates**.

------------------------------------------------------------------------

## Vérifications après l'import

Après l'import de la ressource sur data.gouv.fr, il est recommandé de vérifier que les données ont été correctement interprétées par la
plateforme.

Une **prévisualisation du fichier** est généralement générée **environ 15 minutes après l'import**.

Vérifier notamment :

-   la **prévisualisation du fichier**
-   la bonne **lecture des colonnes**
-   l'absence de **valeurs tronquées ou transformées**
-   la bonne **interprétation des données géographiques** si une carte
    est générée

### Vérifications techniques (avancé)

Il est également possible de vérifier l'absence d'erreur dans les **métadonnées de la ressource** :

-   ouvrir l'onglet **Métadonnées**
-   consulter la section **Extras**
-   vérifier qu'aucune variable **`error`** n'est présente

Il est également possible de vérifier si le traitement de la ressource a été réalisé via la requête :

    /api/1/datasets/<dataset_id>/resources/<resource_id>/crawl

------------------------------------------------------------------------

# Erreurs fréquemment rencontrées

### Top 3 des erreurs

**1 --- Suppression du zéro initial**

Exemple :

    06088 → 6088

Solution : définir le format de cellule **Code postal** avant l'export
CSV.

------------------------------------------------------------------------

**2 --- SIRET affiché en notation scientifique**

Exemple :

    55210055400013 → 5,52101E+13

Solution : définir un format de cellule **Personnalisé** :

    00000000000000

------------------------------------------------------------------------

**3 --- Nom de champ supérieur à 63 caractères**

Conséquence :\
Le fichier peut ne pas être analysé correctement et certaines
**datavisualisations ne seront pas disponibles**.

Solution :

-   raccourcir le nom du champ
-   documenter le champ dans un **fichier de description des variables**

------------------------------------------------------------------------

# Normalisation générale

## Format du fichier

Utiliser **CSV** (format ouvert, non propriétaire).

Sur data.gouv.fr, ce format permet la génération des **prévisualisations** et des **datavisualisations automatisées**.

------------------------------------------------------------------------

## Nom des champs

### Longueur

Les noms de champs doivent comporter **moins de 63 caractères**.

Au-delà, le fichier peut ne pas être analysé correctement.

------------------------------------------------------------------------

### Caractères autorisés

Utiliser uniquement :

-   lettres
-   chiffres
-   `_`
-   `-`

Les espaces, majuscules et caractères spéciaux peuvent compliquer l'interopérabilité.

------------------------------------------------------------------------

# Données géographiques

Pour les référencements territoriaux, s'appuyer sur le **Code officiel géographique (COG)** :

https://www.insee.fr/fr/information/2560452

Exemples de variables :

    code_commune
    code_canton
    code_departement
    code_region
    code_arrondissement
    code_pays
    codes_communes_outre_mer

------------------------------------------------------------------------

## Code commune INSEE

Utiliser le **code commune du COG publié par l'INSEE**, via `code_commune`.

Le **code postal** n'est pas recommandé car un même code postal peut correspondre à plusieurs communes.

### Paramétrage sous Excel

Format de cellule :

    Format de cellule → Spécial → Code postal

Objectif : conserver les **zéros initiaux**.

------------------------------------------------------------------------

# SIRET (14 caractères)

Référence :\
https://annuaire-entreprises.data.gouv.fr/definitions/numero-siret

Paramétrage sous Excel :

    Format de cellule → Personnalisé
    00000000000000

Objectif : conserver les **14 chiffres** et les **zéros initiaux**.

------------------------------------------------------------------------

# SIREN (9 caractères)

Référence :\
https://annuaire-entreprises.data.gouv.fr/definitions/numero-siren

Paramétrage sous Excel :

    Format de cellule → Personnalisé
    000000000

Objectif : conserver les **9 chiffres**.

------------------------------------------------------------------------

# Valeurs nulles et zéros

Dans un jeu de données :

-   `0` signifie **une valeur connue égale à zéro**
-   une cellule vide signifie **information non renseignée**

Il est recommandé de :

-   ne pas utiliser `0` pour représenter une valeur manquante
-   laisser la cellule **vide** si l'information n'est pas disponible
-   documenter les conventions utilisées dans le **fichier de
    description des variables**
