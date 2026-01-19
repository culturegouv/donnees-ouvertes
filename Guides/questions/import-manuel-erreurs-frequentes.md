# Import manuel d’une ressource sur data.gouv : erreurs fréquentes (CSV, codes, SIRET)

Cette fiche recense les erreurs les plus courantes lors de l’import manuel d’une ressource (fichier) sur data.gouv.fr, et les bonnes pratiques associées.

## 1) Privilégier le format CSV
- Utiliser **CSV** (format ouvert, non propriétaire).

## 2) Données géographiques
- Pour les référencements territoriaux, s’appuyer sur le **Code officiel géographique (COG)** : https://www.insee.fr/fr/information/2560452
Cette nomenclature de référence rassemble les codes et libellés, au 1er janvier de l’année en cours, des communes, cantons, arrondissements, départements, collectivités territoriales ayant les compétences départementales, régions et pays et territoires étrangers.

### 2.1) Code commune INSEE (COM) : privilégier le code commune INSEE (plutôt que le code postal)

- Pour identifier une commune, utiliser le **code commune INSEE** (variable `COM`).
- Le **code postal** n’est pas recommandé : **un même code postal peut correspondre à plusieurs communes** (et inversement).

#### Paramétrer le format sous Excel 
Dans Excel, définir le format de cellule : **Format de cellule** → **Spécial** → **Code postal**
Objectif : éviter la perte des zéros initiaux (ex. 06000 transformé en 6000).

### 2.2) Si le code postal est utilisé (non recommandé)
Le **code postal** n’est pas recommandé : **un même code postal peut correspondre à plusieurs communes** (et inversement).
#### Paramétrer le format sous Excel 
- Dans Excel, définir le format de cellule : **Format de cellule** → **Spécial** → **Code postal**
- Objectif : éviter la perte des **zéros initiaux** (ex. `06000` transformé en `6000`).

## 3) SIRET (14 caractères)
- Dans Excel, définir le format de cellule :
  - **Format de cellule** → **Personnalisé**
  - Masque : `00000000000000` (14 zéros)
- Objectif : conserver les **14 chiffres** et les **zéros initiaux**.
