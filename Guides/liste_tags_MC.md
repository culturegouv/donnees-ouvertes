# Principaux tags utilisés par le ministère de la Culture pour la transversale des données de la Culture

Ce document présente les tags recommandés pour décrire les jeux de données publiés dans la transversale « culture ». L’objectif: améliorer la découvrabilité (recherche, filtres), faciliter la réutilisation et garantir une indexation cohérente.

## Règles de taggage

### Tags obligatoires
- `culture`: à ajouter sur tous les jeux de données référencés dans la transversale culture. :contentReference[oaicite:2]{index=2}
- `ministeredelaculture`: à ajouter si le jeu de données est produit par le ministère de la Culture (administration centrale) ou par ses services déconcentrés (DRAC). :contentReference[oaicite:3]{index=3}

### Bonnes pratiques
- privilégier les tags existants de cette liste: avant de créer un nouveau tag, vérifier qu’un tag proche n’existe pas déjà
- rester sobre: 2 à 6 tags bien choisis valent mieux qu’une liste trop longue
- écrire en minuscules, sans accents, au format `kebab-case` (mots séparés par des tirets), par exemple `spectacle-vivant`
- choisir des tags “thématiques” (de quoi parle la donnée) plutôt que des tags “techniques” (csv, api, etc.)

## Liste des tags recommandés

### Jeux du ministère de la Culture
- `ministeredelaculture`

### Thématiques transversales
- `financement`
- `ia` :contentReference[oaicite:5]{index=5}

### DGMIC
- `industries-culturelles`
- `livre`
- `langue`
- `presse` :contentReference[oaicite:6]{index=6}

### DGCA
- `arts-plastiques`
- `spectacle-vivant` :contentReference[oaicite:7]{index=7}

### DGPA
- `architecture`
- `patrimoine`
- `monuments-historiques`
- `sites-patrimoniaux`
- `musee`
- `archives` :contentReference[oaicite:8]{index=8}

### Autres thématiques (selon le périmètre du jeu de données)
- `cinema`

## exemples

- un jeu produit par une DRAC sur des monuments historiques:
  - `culture`, `ministeredelaculture`, `monuments-historiques`, `patrimoine`

- un jeu sur le financement public de structures culturelles:
  - `culture`, `financement` (et `ministeredelaculture` si producteur ministère/DRAC)

- un jeu sur la programmation de spectacle vivant:
  - `culture`, `spectacle-vivant` (et `ministeredelaculture` si producteur ministère/DRAC)

## proposer un nouveau tag

Si un besoin récurrent n’est pas couvert par la liste:
- proposer un tag au format `kebab-case` (sans accents)
- décrire en une phrase son périmètre (ce qu’il couvre / ne couvre pas)
- ouvrir une issue ou une pull request sur le dépôt avec l’ajout à cette liste
