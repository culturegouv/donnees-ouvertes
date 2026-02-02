# Documentation — Scripts et production des données (`data/`)

## Vue d’ensemble

Les fichiers du répertoire `data/` sont **générés automatiquement** :

- à partir des scripts du répertoire `script/` ;
- et, dans certains cas, via l’exécution de **workflows GitHub Actions**.

> ⚠️ Les fichiers produits dans `data/` sont considérés comme des **artefacts générés** :  
> ils ne doivent pas être modifiés manuellement, sauf mention explicite.

---

## Règles de format des fichiers

### CSV et séparateur

Les fichiers CSV générés utilisent le séparateur **point-virgule** (`;`), conformément aux recommandations de data.gouv.fr.

### Encodage (recommandation)

Sauf mention contraire, privilégier un encodage **UTF-8**.

---

## Catalogue général des données du ministère de la Culture

Cette partie concerne les fichiers permettant la génération du **catalogue général des données**.

### Script de génération

- Script : `script/catalogue_MC.py`  
  https://github.com/culturegouv/donnees-ouvertes/blob/main/script/catalogue_MC.py

### Automatisation (mise à jour quotidienne)

- Workflow GitHub Actions : `update-catalogue.yml` (exécution quotidienne)  
  https://github.com/culturegouv/donnees-ouvertes/blob/main/.github/workflows/update-catalogue.yml

### Diffusion / jeu de données cible

Les fichiers générés sont utilisés pour alimenter le jeu de données suivant sur data.gouv.fr :

- Jeu de données :  
  https://www.data.gouv.fr/datasets/61b4226ca5919d3b718b8e9e

---

## Bonnes pratiques de contribution

### Ajouter un nouveau fichier généré

1. Identifier la source (API, fichier amont, extraction).
2. Ajouter/mettre à jour le script de génération dans `script/`.
3. Si une mise à jour régulière est nécessaire :
   - créer ou compléter un workflow GitHub Actions,
   - documenter la fréquence et le déclencheur (manuel, quotidien, etc.).
4. Documenter :
   - le nom du fichier généré,
   - le script associé,
   - le workflow associé (si applicable),
   - le format (CSV, séparateur, encodage),
   - le jeu de données data.gouv.fr associé (si applicable).

### Éviter les modifications manuelles dans `data/`

Si une correction est nécessaire, elle doit être faite **à la source** :
- dans le script,
- ou dans la configuration du workflow,
puis régénérée via le processus automatisé.

---

## Références utiles

- Répertoire des scripts :  
  https://github.com/culturegouv/donnees-ouvertes/tree/main/script
- Répertoire des workflows GitHub :  
  https://github.com/culturegouv/donnees-ouvertes/tree/main/.github/workflows
- Répertoire des données générées :  
  https://github.com/culturegouv/donnees-ouvertes/tree/main/data
