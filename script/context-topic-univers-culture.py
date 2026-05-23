# -*- coding: utf-8 -*-
import csv
import os
from datetime import datetime, timezone

import pandas as pd
from datagouv import Client, Topic

TOPIC_ID = "univers-culture"
ENVIRONMENT = "www"  # "www" (prod), "demo" ou "dev"
OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)


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


def build_catalog_for_topic(topic_id, client):
    rows = []
    generated_at = datetime.now(timezone.utc).isoformat()

    topic = Topic(topic_id, _client=client)

    for dataset in topic.datasets:
        for resource in dataset.resources:
            # resource.profile lève une exception si la ressource n'est pas APIfiée
            try:
                profile_payload = resource.profile
            except Exception as exc:
                print(f"Profil tabulaire indisponible {resource.id} : {exc}")
                continue

            # Le client renvoie le payload complet de l'API tabulaire,
            # qui contient une clé "profile" wrappant header/columns/profile.
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
