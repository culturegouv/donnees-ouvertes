# Principaux tags utilisés par le ministère de la Culture pour la transversale des données de la Culture

Ce document présente les tags recommandés pour décrire les jeux de données publiés dans la transversale des données de la Culture (`culture.data.gouv.fr`) et sur `data.gouv.fr`.

L’objectif: améliorer la découvrabilité (recherche, filtres), faciliter la réutilisation et garantir une indexation cohérente. Cette liste n’est ni limitative ni exhaustive: elle peut évoluer et être complétée en fonction des besoins des producteurs et des usages.

## Règles de taggage

### Tags à appliquer pour le référencement dans la transversale
- `culture`: à ajouter sur tous les jeux de données référencés dans la transversale culture
- `ministeredelaculture`: à utiliser lorsque le jeu de données est produit par le ministère de la Culture (administration centrale), ses services déconcentrés (DRAC), ou par un opérateur ou établissement public rattaché au ministère

note: les opérateurs et établissements publics rattachés au ministère peuvent également utiliser le tag `ministeredelaculture`.

### Bonnes pratiques
- privilégier les tags existants de cette liste: avant de créer un nouveau tag, vérifier qu’un tag proche n’existe pas déjà
- rester sobre: 2 à 6 tags bien choisis valent mieux qu’une liste trop longue
- écrire en minuscules, sans accents, au format `kebab-case` (mots séparés par des tirets), par exemple `spectacle-vivant`
- choisir des tags thématiques (de quoi parle la donnée) plutôt que des tags techniques (csv, api, etc.)

## Liste des tags recommandés (ordre alphabétique)
- `architecture`
- `archives`
- `arts-plastiques`
- `cinema`
- `financement`
- `ia`
- `industries-culturelles`
- `langue`
- `livre`
- `ministeredelaculture`
- `monuments-historiques`
- `musee`
- `patrimoine`
- `presse`
- `sites-patrimoniaux`
- `spectacle-vivant`

## Exemples
- un jeu produit par une DRAC sur des monuments historiques: `culture`, `ministeredelaculture`, `monuments-historiques`, `patrimoine`
- un jeu sur le financement public de structures culturelles: `culture`, `financement` (et `ministeredelaculture` si producteur ministère/DRAC/opérateur rattaché)
- un jeu sur la programmation de spectacle vivant: `culture`, `spectacle-vivant` (et `ministeredelaculture` si producteur ministère/DRAC/opérateur rattaché)

## Proposer un nouveau tag
Un nouveau tag est ajouté lorsqu’il correspond à plusieurs jeux de données ou à une politique publique structurante, afin d’éviter la multiplication de tags synonymes

Si un besoin récurrent n’est pas couvert par la liste:
- proposer un tag au format `kebab-case` (sans accents)
- décrire en une phrase son périmètre (ce qu’il couvre / ne couvre pas)
- ouvrir une issue ou une pull request sur le dépôt (ou contacter l’équipe en charge de la transversale) pour proposer l’ajout à cette liste
