# -*- coding: utf-8 -*-
import csv
import os
import time
from datetime import datetime, timezone

import pandas as pd
import requests
from datagouv import Client, Topic

TOPIC_ID = "univers-culture"
ENVIRONMENT = "www"  # "www" (prod), "demo" ou "dev"
OUTPUT_DIR = "data"

TABULAR_API_BASE = "https://tabular-api.data.gouv.fr/api/resources"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 2
RETRY_BACKOFF = 2  # secondes

os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_profile(resource_id, session):
    """Récupère le profil tabulaire via l'API Tabular.
    Retourne None si la ressource n'est pas APIfiée ou en cas d'erreur."""
    url = f"{TABULAR_API_BASE}/{resource_id}/profile/"

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as exc:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            print(f"Profil indisponible {resource_id} : {exc}")
            return None

        if response.status_code == 404:
            # Ressource non exposée par l'API tabulaire : silencieux
            return None

        if response.status_code >= 500 and attempt < MAX_RETRIES:
            time.sleep(RETRY_BACKOFF * (attempt + 1))
            continue

        if not response.ok:
            print(f"Profil indisponible {resource_id} : HTTP {response.status_code}")
            return None

        # Vérifie qu'on a bien du JSON (pas une page d'erreur HTML)
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type.lower():
            print(f"Profil indisponible {resource_id} : réponse non-JSON ({content_type})")
            return None

        try:
            return response.json()
        except ValueError as exc:
            print(f"Profil indisponible {resource_id} : JSON invalide ({exc})")
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
        "top_1": tops[0]["value"] if len(tops) > 0 else "",
        "top_2": tops[1]["value"] if len(tops) > 1 else "",
        "top_3": tops[2]["value"] if len(tops) > 2 else "",
    }


def build_catalog_for_topic(topic_id, client, session):
    rows = []
    generated_at = datetime.now(timezone.utc).isoformat()

    topic = Topic(topic_id, _client=client)

    for dataset in topic.datasets:
        for resource in dataset.resources:
            profile_payload = fetch_profile(resource.id, session)
            if profile_payload is None:
                continue

            # L'API renvoie { "profile": { "header": [...], "columns": {...}, "profile": {...} } }
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

    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})
        df = build_catalog_for_topic(TOPIC_ID, client, session)

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
