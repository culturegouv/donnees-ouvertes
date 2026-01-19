# Absence de la vue Explore après l’ajout ou la mise à jour d’une ressource

## Objet

Cette procédure décrit les vérifications à effectuer lorsqu’une ressource (souvent un fichier CSV) ajoutée ou mise à jour sur data.gouv.fr ne s’affiche pas dans la vue **Explore** (prévisualisation et exploration des données).

## Pré-requis

- disposer de l’**identifiant de la ressource** (`resource_id`, au format UUID)
- connaître l’URL du **jeu de données** concerné (ou son `dataset_id`)

---

## 1. Vérifier l’affichage dans Explore

Il est possible de tester l’affichage directement dans Explore via une URL de la forme :

`https://explore.data.gouv.fr/fr/datasets/<dataset_id>/#/resources/<resource_id>`

Exemples :

- <https://explore.data.gouv.fr/fr/datasets/5af120e5b595087cfabcde81/#/resources/3a52af4a-f9da-4dcc-8110-b07774dfb3bc>
- <https://explore.data.gouv.fr/fr/datasets/695b8b6f6bf16db672fa28df/#/resources/e4761b32-c601-4ec9-b361-658315d07389>

### Interprétation

- Si le tableau s’affiche correctement dans Explore : la ressource est bien prise en charge par Explore.
- Si Explore ne s’affiche pas (ou reste vide) : poursuivre avec l’étape 2.

---

## 2. Vérifier l’état de traitement de la ressource (crawler)

L’affichage dans Explore dépend d’un traitement automatique (analyse / ingestion) réalisé par le **crawler**.

### 2.1 Interroger l’API du crawler

Utiliser l’URL suivante en remplaçant `ID_RESSOURCE` par l’identifiant de la ressource :

`https://crawler.data.gouv.fr/api/resources/ID_RESSOURCE`

Exemple :

- <https://crawler.data.gouv.fr/api/resources/e4761b32-c601-4ec9-b361-658315d07389>

### 2.2 Interpréter le statut

Si la réponse contient un statut de ce type :

```json
{
  "dataset_id": "695b8b6f6bf16db672fa28df",
  "resource_id": "e4761b32-c601-4ec9-b361-658315d07389",
  "status": "TO_ANALYSE_RESOURCE",
  "status_since": "2026-01-19T11:37:39.063939+00:00"
}
```

attendre la fin du traitement, et tester à nouveay ensuite l’URL Explore (étape 1).

Cas B — Analyse qui semble bloquée (statut inchangé durablement)

Si le statut ne semble pas évoluer après un délai raisonnable, contacter le support / l’équipe technique en fournissant :

- l’URL du jeu de données (data.gouv.fr),
- le resource_id,
- l’URL Explore testée,
- l’URL crawler testée,



