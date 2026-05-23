# -*- coding: utf-8 -*-
"""
Génère un catalogue de schémas tabulaires pour un topic data.gouv.fr.
Produit deux fichiers CSV : un par dataset, un par colonne profilée.

Usage :
    TOPIC_SLUG=univers-culture-deps python script/catalog-topic.py
"""
import csv
import json
import os
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

# --- Configuration ---
TOPIC_SLUG = os.environ.get("TOPIC_SLUG", "univers-culture-deps")
OUTPUT_DIR = "data"

DATAGOUV_API = "https://www.data.gouv.fr/api"
TABULAR_API_BASE = "https://tabular-api.data.gouv.fr/api/resources"

TABULAR_FORMATS = {"csv", "xls", "xlsx"}
MIN_DATE = datetime(2020, 1, 1, tzinfo=timezone.utc)
ONLY_MAIN_RESOURCES = True

REQUEST_TIMEOUT = 15
MAX_RETRIES = 1
RETRY_BACKOFF = 2
PROGRESS_EVERY = 25

os.makedirs(OUTPUT_DIR, exist_ok=True)


def log(msg):
    print(msg, flush=True)


def http_get_json(url):
    """GET d'un JSON avec retry simple. Retourne None en cas d'échec."""
    req = Request(url, headers={"Accept": "application/json"})
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code >= 500 and attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            log(f"  HTTP {exc.code} sur {url}")
            return None
        except (URLError, TimeoutError) as exc:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            log(f"  Erreur réseau sur {url} : {exc}")
            return None
        except ValueError as exc:
            log(f"  JSON invalide sur {url} : {exc}")
            return None
    return None


def parse_dt(value):
    """Parse une date ISO 8601, retourne None si invalide."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def normalize_format(fmt):
    """Normalise les variantes de formats déclarés."""
    fmt = (fmt or "").lower().strip()
    if "spreadsheetml" in fmt or "microsoft excel" in fmt:
        return "xlsx"
    if fmt.startswith("csv"):
        return "csv"
    return fmt


def get_topic_dataset_ids(topic_slug):
    """Récupère tous les dataset_ids d'un topic via pagination."""
    dataset_ids = []
    page = 1
    page_size = 100

    while True:
        url = f"{DATAGOUV_API}/2/topics/{topic_slug}/elements/?page={page}&page_size={page_size}"
        data = http_get_json(url)
        if data is None:
            break

        for item in data.get("data", []) or []:
            element = item.get("element") or {}
            if element.get("class") == "Dataset" and element.get("id"):
                dataset_ids.append(element["id"])

        if not data.get("next_page"):
            break
        page += 1

    return dataset_ids


def fetch_dataset(dataset_id):
    """Récupère un dataset complet avec ses ressources."""
    return http_get_json(f"{DATAGOUV_API}/1/datasets/{dataset_id}/")


def fetch_profile(resource_id):
    """Récupère le profil tabulaire via l'API Tabular."""
    url = f"{TABULAR_API_BASE}/{resource_id}/profile/"
    return http_get_json(url)


def is_recent_enough(resource):
    last_mod = parse_dt(resource.get("last_modified"))
    created = parse_dt(resource.get("created_at"))
    candidates = [d for d in (last_mod, created) if d is not None]
    if not candidates:
        return True
    return max(candidates) >= MIN_DATE


def build_dataset_row(*, generated_at, topic_slug, dataset):
    return {
        "generated_at": generated_at,
        "topic_id": topic_slug,
        "id.dataset": dataset.get("id", ""),
        "title.dataset": dataset.get("title", "") or "",
        "description.dataset": dataset.get("description", "") or "",
        "tags.dataset": ";".join(str(t) for t in (dataset.get("tags") or [])),
        "created_at.dataset": dataset.get("created_at", "") or "",
        "last_modified.dataset": dataset.get("last_modified", "") or "",
        "archived.dataset": dataset.get("archived", "") or "",
    }


def build_column_row(*, generated_at, topic_slug, dataset, resource, column_name, col_meta, col_stats):
    tops = col_stats.get("tops", []) or []
    return {
        "generated_at": generated_at,
        "topic_id": topic_slug,
        "id.dataset": dataset.get("id", ""),
        "id.ressource": resource.get("id", ""),
        "title.ressource": resource.get("title", "") or "",
        "format.ressource": resource.get("format", "") or "",
        "url.ressource": resource.get("url", "") or "",
        "created_at.ressource": resource.get("created_at", "") or "",
        "last_modified.ressource": resource.get("last_modified", "") or "",
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


def build_catalog_for_topic(topic_slug):
    schema_rows = []
    datasets_rows = []
    generated_at = datetime.now(timezone.utc).isoformat()
    start_time = time.monotonic()

    resources_seen = 0
    resources_filtered_format = 0
    resources_filtered_date = 0
    resources_filtered_type = 0
    resources_tested = 0
    resources_profiled = 0
    datasets_archived = 0

    log(f"Récupération des datasets du topic '{topic_slug}'...")
    dataset_ids = get_topic_dataset_ids(topic_slug)
    log(f"{len(dataset_ids)} datasets trouvés dans le topic\n")

    for i, did in enumerate(dataset_ids, start=1):
        dataset = fetch_dataset(did)
        if dataset is None:
            log(f"[{i}/{len(dataset_ids)}] {did} - dataset introuvable")
            continue

        title = dataset.get("title", "") or ""
        log(f"[{i}/{len(dataset_ids)}] {did} - {title}")

        datasets_rows.append(
            build_dataset_row(generated_at=generated_at, topic_slug=topic_slug, dataset=dataset)
        )

        if dataset.get("archived"):
            datasets_archived += 1
            continue

        for resource in dataset.get("resources", []) or []:
            resources_seen += 1

            fmt = normalize_format(resource.get("format"))
            if fmt not in TABULAR_FORMATS:
                resources_filtered_format += 1
                continue

            if ONLY_MAIN_RESOURCES:
                rtype = (resource.get("type") or "").lower()
                if rtype and rtype != "main":
                    resources_filtered_type += 1
                    continue

            if not is_recent_enough(resource):
                resources_filtered_date += 1
                continue

            resources_tested += 1
            profile_payload = fetch_profile(resource.get("id"))
            if profile_payload is None:
                continue

            resources_profiled += 1
            profile = profile_payload.get("profile", profile_payload)
            header = profile.get("header", []) or []
            columns = profile.get("columns", {}) or {}
            stats = profile.get("profile", {}) or {}

            for column_name in header:
                schema_rows.append(
                    build_column_row(
                        generated_at=generated_at,
                        topic_slug=topic_slug,
                        dataset=dataset,
                        resource=resource,
                        column_name=column_name,
                        col_meta=columns.get(column_name, {}) or {},
                        col_stats=stats.get(column_name, {}) or {},
                    )
                )

        if i % PROGRESS_EVERY == 0:
            elapsed = time.monotonic() - start_time
            log(
                f"  → progression : {i}/{len(dataset_ids)} datasets, "
                f"{resources_seen} ressources vues, "
                f"{resources_tested} testées, "
                f"{resources_profiled} profilées, "
                f"{len(schema_rows)} colonnes — {elapsed:.0f}s"
            )

    elapsed = time.monotonic() - start_time
    log(
        f"\nTerminé en {elapsed:.0f}s."
        f"\n  Datasets : {len(datasets_rows)} (dont {datasets_archived} archivés)"
        f"\n  Ressources vues       : {resources_seen}"
        f"\n  Exclues (format)      : {resources_filtered_format}"
        f"\n  Exclues (type)        : {resources_filtered_type}"
        f"\n  Exclues (date <{MIN_DATE.year}) : {resources_filtered_date}"
        f"\n  Testées               : {resources_tested}"
        f"\n  Profilées             : {resources_profiled}"
        f"\n  Colonnes documentées  : {len(schema_rows)}"
    )

    return pd.DataFrame(schema_rows), pd.DataFrame(datasets_rows)


if __name__ == "__main__":
    df_schema, df_datasets = build_catalog_for_topic(TOPIC_SLUG)

    schema_file = f"{OUTPUT_DIR}/catalog_schema_{TOPIC_SLUG}.csv"
    datasets_file = f"{OUTPUT_DIR}/catalog_datasets_{TOPIC_SLUG}.csv"

    df_schema.to_csv(schema_file, index=False, quoting=csv.QUOTE_ALL, quotechar='"', encoding="utf-8")
    df_datasets.to_csv(datasets_file, index=False, quoting=csv.QUOTE_ALL, quotechar='"', encoding="utf-8")

    log(f"\nFichier généré : {schema_file} ({len(df_schema)} colonnes)")
    log(f"Fichier généré : {datasets_file} ({len(df_datasets)} datasets)")
