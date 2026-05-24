# -*- coding: utf-8 -*-
"""
⚠️ SCRIPT DÉPRÉCIÉ — ne plus utiliser.

Remplacé le 24 mai 2026 par `script/catalog-topic.py`, qui interroge
directement l'API REST data.gouv.fr (endpoints v2/topics et v1/datasets)
au lieu de passer par le SDK `datagouv-client`.

Motif du remplacement :
- Le SDK fait un appel HTTP par dataset lors de l'itération `topic.datasets`
  (chaque `Dataset(id)` déclenche un `refresh()` qui appelle `/api/1/datasets/<id>/`).
- Sur les gros topics (~1000 datasets), l'enchaînement de requêtes via
  `httpx` finit régulièrement par échouer sur `RemoteProtocolError:
  Server disconnected without sending a response` après une dizaine de minutes.
- Le run automatique du 24/05/2026 06:00 UTC a échoué après 13 min sur ce motif,
  alors que le run manuel de la veille avait pourtant réussi en ~1h sur le même
  topic (`univers-culture`, ~1050 datasets).

Le workflow associé (`.github/workflows/update-topic-context.yml`) a été
supprimé à la même date. Voir le nouveau workflow
`update-topic-catalog.yml` pour le remplacement.

Conservé en l'état pour traçabilité — à supprimer définitivement après
plusieurs semaines de runs réussis sur le nouveau script.
"""


import csv
import json
import os
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd
from datagouv import Client, Topic

TOPIC_ID = "univers-culture"
ENVIRONMENT = "www"
OUTPUT_DIR = "data"

TABULAR_API_BASE = "https://tabular-api.data.gouv.fr/api/resources"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 2
RETRY_BACKOFF = 2

os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_profile(resource_id):
    """Récupère le profil tabulaire via l'API Tabular.
    Retourne None si la ressource n'est pas APIfiée ou en cas d'erreur."""
    url = f"{TABULAR_API_BASE}/{resource_id}/profile/"
    req = Request(url, headers={"Accept": "application/json"})

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                content_type = response.headers.get("Content-Type", "")
                if "json" not in content_type.lower():
                    print(f"Profil indisponible {resource_id} : réponse non-JSON ({content_type})")
                    return None
                try:
                    return json.loads(response.read().decode("utf-8"))
                except ValueError as exc:
                    print(f"Profil indisponible {resource_id} : JSON invalide ({exc})")
                    return None

        except HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code >= 500 and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            print(f"Profil indisponible {resource_id} : HTTP {exc.code}")
            return None

        except URLError as exc:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            print(f"Profil indisponible {resource_id} : {exc.reason}")
            return None

    return None


def extract_column_row(
    *,
    generated_at,
    topic_id,
    dataset,
    resource,
    column_name,
    col_meta,
    col_stats,
):
    tops = col_stats.get("tops", []) or []
    return {
        "generated_at": generated_at,
        "topic_id": topic_id,
        "id.dataset": dataset.id,
        "id.ressource": resource.id,
        "title.dataset": getattr(dataset, "title", "") or "",
        "description.dataset": getattr(dataset, "description", "") or "",
        "tags.dataset": ";".join(str(t) for t in (getattr(dataset, "tags", []) or [])),
        "title.ressource": getattr(resource, "title", "") or "",
        "format.ressource": getattr(resource, "format", "") or "",
        "url.ressource": getattr(resource, "url", "") or "",
        "column_name": column_name,
        "column_datatype": col_meta.get("format", ""),
        "python_type": col_meta.get("python_type", ""),
        "score": col_meta.get("score", ""),
        "nb_distinct": col_stats.get("nb_distinct", ""),
        "nb_missing_values": col_stats.get("nb_missing_values", ""),
        "top_1": tops[0].get("value", "") if len(tops) > 0 and isinstance(tops[0], dict) else "",
        "top_2": tops[1].get("value", "") if len(tops) > 1 and isinstance(tops[1], dict) else "",
        "top_3": tops[2].get("value", "") if len(tops) > 2 and isinstance(tops[2], dict) else "",
    }


def build_catalog_for_topic(topic_id, client):
    rows = []
    generated_at = datetime.now(timezone.utc).isoformat()

    topic = Topic(topic_id, _client=client)
    datasets = list(topic.datasets)
    print(f"{len(datasets)} datasets trouvés dans le topic {topic_id}")

    for i, dataset in enumerate(datasets, start=1):
        print(f"[{i}/{len(datasets)}] {dataset.id} - {getattr(dataset, 'title', '')}")
        for resource in getattr(dataset, "resources", []) or []:
            profile_payload = fetch_profile(resource.id)
            if profile_payload is None:
                continue

            profile = profile_payload.get("profile", profile_payload)
            header = profile.get("header", []) or []
            columns = profile.get("columns", {}) or {}
            stats = profile.get("profile", {}) or {}

            for column_name in header:
                rows.append(
                    extract_column_row(
                        generated_at=generated_at,
                        topic_id=topic_id,
                        dataset=dataset,
                        resource=resource,
                        column_name=column_name,
                        col_meta=columns.get(column_name, {}) or {},
                        col_stats=stats.get(column_name, {}) or {},
                    )
                )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    client = Client(environment=ENVIRONMENT, timeout=60)
    df = build_catalog_for_topic(TOPIC_ID, client)

    output_file = f"{OUTPUT_DIR}/schema_topic_{TOPIC_ID}.csv"
    df.to_csv(
        output_file,
        index=False,
        quoting=csv.QUOTE_ALL,
        quotechar='"',
        encoding="utf-8",
    )

    print(f"Fichier généré : {output_file}")
    print(f"{len(df)} propriétés documentées")
