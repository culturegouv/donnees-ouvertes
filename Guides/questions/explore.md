

1) Vérifier si le fichier s'affiche dans Explore : 

Exemple d'URL 1 : 
https://explore.data.gouv.fr/fr/datasets/5af120e5b595087cfabcde81/#/resources/3a52af4a-f9da-4dcc-8110-b07774dfb3bc

Exemple d'URL 2 : 
https://explore.data.gouv.fr/fr/datasets/695b8b6f6bf16db672fa28df/#/resources/e4761b32-c601-4ec9-b361-658315d07389


2) Si le fichier ne s'affiche pas : 

Vérifier que le crawler a terminer la tâche : https://crawler.data.gouv.fr/api/resources/**ID_ressource**

Exemple 
https://crawler.data.gouv.fr/api/resources/e4761b32-c601-4ec9-b361-658315d07389

Si {"dataset_id": "695b8b6f6bf16db672fa28df", "resource_id": "e4761b32-c601-4ec9-b361-658315d07389", "status": "TO_ANALYSE_RESOURCE", "status_since": "2026-01-19T11:37:39.063939+00:00"}
Alors la ressource est encore en cours d'analyse
