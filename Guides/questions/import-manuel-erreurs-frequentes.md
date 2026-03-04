# Guide de bonnes pratiques pour formater une ressource avant son import sur data.gouv.fr

Cette fiche présente les bonnes pratiques à respecter lors du formatage et de l'import manuel d'une ressource (fichier) sur data.gouv.fr. Elle vise à faciliter l'exploitation des données sur la plateforme, notamment la génération des **prévisualisations** et des **datavisualisations automatiques**.

---

## Sommaire

- [Bonnes pratiques de formatage](#1-bonnes-pratiques-de-formatage)
- [Vérifications avant et après l'import](#2-vérifications-avant-et-après-limport)
- [Erreurs fréquemment rencontrées](#3-erreurs-fréquemment-rencontrées)
- [Normalisation générale](#4-normalisation-générale)
- [Données géographiques](#5-données-géographiques)
- [SIRET](#6-siret)
- [SIREN](#7-siren)
- [Valeurs nulles et zéros](#8-valeurs-nulles-et-zéros)

---

## 1. Bonnes pratiques de formatage

### Principes généraux

- Utiliser le format **CSV**
- Utiliser des **noms de champs simples**, sans espaces ni caractères spéciaux (sauf `_` ou `-`)
- Limiter les noms de champs à **63 caractères**
- Utiliser le **code commune INSEE** pour les référencements territoriaux
- Utiliser des colonnes distinctes pour les **identifiants d'entreprises** (`SIREN`, `SIRET`)
- Utiliser **une seule feuille par fichier**
- Utiliser une **structure tabulaire simple**, sans cellules fusionnées
- Les **couleurs et mises en forme Excel ne sont pas prises en compte**
- Privilégier l'**alignement avec des référentiels et vocabulaires**
- Principe : **une colonne = une information**

---

## 2. Vérifications avant et après l'import

Certaines transformations automatiques peuvent être appliquées par les tableurs (Excel, LibreOffice, etc.) lors de la préparation ou de l'export d'un fichier.

### 2.1 Vérifications avant l'import

#### Codes géographiques
Vérifier que les **zéros initiaux sont conservés**.

```
06088 → 6088
```

#### Identifiants d’entreprises
Vérifier que les **SIREN et SIRET ne sont pas affichés en notation scientifique**.

```
55210055400013 → 5,52101E+13
```

#### Pourcentages
Vérifier qu’aucune conversion automatique n’a été appliquée.

```
2 % → 0,02
```

#### Dates
Vérifier que certaines valeurs n’ont pas été **interprétées automatiquement comme des dates**.

---

### 2.2 Vérifications après l'import

Une **prévisualisation du fichier** est généralement disponible **environ 15 minutes après l'import**.

Vérifier :
- la **prévisualisation du fichier**
- la bonne **lecture des colonnes**
- l'absence de **valeurs transformées**
- la bonne **interprétation des données géographiques**

#### Vérifications techniques (avancé)

Dans **Métadonnées → Extras**, vérifier qu'aucune variable `error` n'est présente.

Il est également possible de vérifier le traitement de la ressource via :

```
/api/1/datasets/<dataset_id>/resources/<resource_id>/crawl
```

---

## 3. Erreurs fréquemment rencontrées

### Top 3 des erreurs

#### 1. Suppression du zéro initial

```
06088 → 6088
```

Solution : utiliser le format **Code postal** dans Excel.

---

#### 2. SIRET affiché en notation scientifique

```
55210055400013 → 5,52101E+13
```

Solution : définir un format personnalisé :

```
00000000000000
```

---

#### 3. Nom de champ supérieur à 63 caractères

Conséquence : certaines **datavisualisations ne seront pas générées**.

Solution :
- raccourcir le nom du champ
- documenter la variable dans un fichier de description

---

## 4. Normalisation générale

### Format du fichier
Utiliser **CSV** (format ouvert, non propriétaire). Ce format permet la génération des **prévisualisations** et **datavisualisations automatiques** sur data.gouv.fr.

### Noms de champs

#### Longueur
Maximum **63 caractères**.

#### Caractères autorisés
- lettres
- chiffres
- `_`
- `-`

Les espaces et caractères spéciaux peuvent provoquer des **erreurs lors de l’analyse du fichier**.

---

## 5. Données géographiques

Pour les référencements territoriaux, utiliser le **Code officiel géographique (COG)** :
https://www.insee.fr/fr/information/2560452

### Exemples de variables

- `code_commune`
- `code_canton`
- `code_departement`
- `code_region`
- `code_arrondissement`
- `code_pays`
- `codes_communes_outre_mer`

### Code commune INSEE
Utiliser `code_commune`. Le **code postal** n'est pas recommandé car un même code postal peut correspondre à plusieurs communes.

#### Paramétrage Excel
```
Format de cellule → Spécial → Code postal
```

---

## 6. SIRET

### SIRET (14 caractères)

Référence :
https://annuaire-entreprises.data.gouv.fr/definitions/numero-siret

Paramétrage Excel :
Format de cellule → Personnalisé
```
00000000000000
```

---

## 7. SIREN

### SIREN (9 caractères)

Référence :
https://annuaire-entreprises.data.gouv.fr/definitions/numero-siren

Paramétrage Excel :
Format de cellule → Personnalisé
```
000000000
```

---

## 8. Valeurs nulles et zéros

Dans un jeu de données :
- `0` signifie **valeur connue égale à zéro**
- une cellule vide signifie **information non renseignée**

Recommandations :
- ne pas utiliser `0` pour représenter une valeur manquante
- laisser la cellule vide si l'information n'est pas disponible
- documenter les conventions dans le fichier de description des variables
