# Explore ne s’affiche pas après l’ajout ou la mise à jour d’une ressource

## Objet
Cette page décrit les vérifications à effectuer lorsque la vue **Explore** (prévisualisation et exploration) ne s’affiche pas après l’ajout ou la mise à jour d’une **ressource** sur data.gouv.fr.

L’affichage dans Explore dépend d’un traitement automatique (analyse / ingestion) opéré par un service de crawl et d’analyse des ressources. Une ressource peut donc être publiée sur data.gouv.fr tout en nécessitant un délai avant d’être exploitable dans Explore.

## Pré-requis
- Disposer de l’identifiant de la ressource (`resource_id`, au format UUID).
- Connaître l’identifiant du jeu de données (`dataset_id`) ou l’URL du jeu de données.

---

## 1) Vérifier l’affichage dans Explore

Tester l’affichage via une URL de la forme :

`https://explore.data.gouv.fr/fr/datasets/<dataset_id>/#/resources/<resource_id>`

Exemples :
- https://explore.data.gouv.fr/fr/datasets/5af120e5b595087cfabcde81/#/resources/3a52af4a-f9da-4dcc-8110-b07774dfb3bc
- https://explore.data.gouv.fr/fr/datasets/695b8b6f6bf16db672fa28df/#/resources/e4761b32-c601-4ec9-b361-658315d07389

### Résultat attendu
- Si le tableau s’affiche : la ressource est bien prise en charge par Explore.
- Si Explore ne s’affiche pas (ou reste vide) : poursuivre avec l’étape 2.

---

## 2) Vérifier l’état d’analyse dans le crawler

L’affichage dans Explore nécessite que la ressource ait été analysée.
Il est possible de consulter l’état de traitement via l’API du crawler.

### 2.1 Consulter l’état de la ressource
Ouvrir l’URL suivante en remplaçant `ID_RESSOURCE` par le `resource_id` :

`https://crawler.data.gouv.fr/api/resources/ID_RESSOURCE`

Exemple :
- https://crawler.data.gouv.fr/api/resources/e4761b32-c601-4ec9-b361-658315d07389

### 2.2 Interpréter le champ `status`
Exemple de réponse (extrait) :

```json
{
  "dataset_id": "695b8b6f6bf16db672fa28df",
  "resource_id": "e4761b32-c601-4ec9-b361-658315d07389",
  "status": "TO_ANALYSE_RESOURCE",
  "status_since": "2026-01-19T11:37:39.063939+00:00"
}
```

Si `status` vaut `TO_ANALYSE_RESOURCE`, cela signifie que la ressource est **en attente d’analyse** : il est normal que Explore ne soit pas encore disponible.

---

## 3) Repères sur les statuts (lecture simplifiée)

Les statuts exacts peuvent évoluer, mais on rencontre typiquement les étapes suivantes :

- `TO_ANALYSE_RESOURCE` : la ressource est en file d’attente pour analyse.
- `ANALYSING_RESOURCE` : analyse de la ressource en cours.
- `TO_ANALYSE_CSV` / `ANALYSING_CSV` : analyse spécifique des contenus tabulaires (CSV).
- `INSERTING_IN_DB` : ingestion en base (préparation de l’exploration).
- `CONVERTING_TO_PARQUET` : conversion dans un format de diffusion (selon le cas).
- `BACKOFF` : ralentissement temporaire (par exemple, limitation côté source).

---

## 4) Actions recommandées

### Cas A — L’analyse est en cours
- Attendre la fin du traitement (les délais varient selon la taille, le format et la complexité du fichier).
- Re-tester ensuite l’URL Explore (étape 1).

### Cas B — Le statut n’évolue pas durablement
Si le statut reste inchangé de manière inhabituelle :
- Préparer les éléments ci-dessous et contacter l’équipe support/technique.

---

## 5) Informations à transmettre au support/technique

- URL du jeu de données (data.gouv.fr)
- `dataset_id` (si disponible)
- `resource_id`
- URL Explore testée
- URL crawler testée
- Réponse JSON complète renvoyée par le crawler



