#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from io import StringIO
from datetime import datetime, timezone

import pandas as pd
import requests

# -------------------------------------------------------------
# Liste des organisations à importer
# -------------------------------------------------------------
ORG_IDS = [
    "534fff91a3a7292c64a77f73",
    "534fff5ea3a7292c64a77d40",
    "534fff5fa3a7292c64a77d49",
    "534fff5fa3a7292c64a77d44",
    "534fff60a3a7292c64a77d55",
    "534fff71a3a7292c64a77dcd",
    "534fff72a3a7292c64a77dd0",
    "534fff73a3a7292c64a77dda",
    "534fff74a3a7292c64a77ddd",
    "534fff74a3a7292c64a77de0",
    "534fff82a3a7292c64a77e82",
    "534fff97a3a7292c64a7800b",
    "534fff98a3a7292c64a7800e",
    "534fffb2a3a7292c64a78125",
    "57fe0dfac751df15a779df72",
]

OUT_PATH = "data/catalogue_culture_global.csv"
LOG_TXT_PATH = "data/catalogue_culture_global_log.txt"
LOG_STATS_PATH = "data/catalogue_culture_global_stats.csv"


# -------------------------------------------------------------
# Logging helper (console + fichier)
# -------------------------------------------------------------
def init_logger(log_txt_path: str):
    os.makedirs(os.path.dirname(log_txt_path), exist_ok=True)
    with open(log_txt_path, "w", encoding="utf-8") as f:
        f.write("")

    def log(msg: str = ""):
        print(msg)
        with open(log_txt_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    return log


# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------
def get_org_info(session: requests.Session, oid: str) -> dict:
    """
    Récupère les infos d'organisation (notamment 'name') via /organizations/<oid>/.
    """
    url = f"https://www.data.gouv.fr/api/1/organizations/{oid}/"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def org_has_at_least_one_dataset(session: requests.Session, oid: str) -> bool:
    """
    Teste si l'organisation a au moins 1 dataset via l'API JSON.
    Pas de pagination nécessaire pour ce test.
    """
    url = f"https://www.data.gouv.fr/api/1/organizations/{oid}/datasets/?page_size=1"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    return bool(payload.get("data"))


def download_org_csv(session: requests.Session, oid: str, log) -> pd.DataFrame:
    """
    Télécharge le CSV datasets.csv pour une organisation et le charge en DataFrame.
    """
    url = f"https://www.data.gouv.fr/api/1/organizations/{oid}/datasets.csv"
    log(f"📥 Téléchargement : {url}")

    r = session.get(url, timeout=60)
    r.raise_for_status()

    df = pd.read_csv(
        StringIO(r.text),
        sep=";",
        quotechar='"',
        engine="python",
        on_bad_lines="warn",
    )
    df["organization_id"] = oid
    return df


def sanitize_for_flat_files(df: pd.DataFrame) -> pd.DataFrame:
    """
    Évite les soucis de rendu/parse en supprimant les retours à la ligne
    à l'intérieur des champs texte (description, etc.).
    """
    obj_cols = df.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.replace(r"[\r\n]+", " ", regex=True)
    return df


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------
def main() -> int:
    log = init_logger(LOG_TXT_PATH)

    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log(f"🕒 Run UTC : {run_ts}")
    log(f"📌 Nombre d'organisations: {len(ORG_IDS)}")
    log("")

    session = requests.Session()

    frames = []
    counts_by_org = {}
    org_name_by_id = {}  # ✅ cache oid -> name

    skipped = 0
    failed = 0

    # ✅ Charger les noms d'org une seule fois (et les réutiliser)
    for oid in ORG_IDS:
        try:
            info = get_org_info(session, oid)
            # .strip() pour éviter les espaces parasites (ex: "Centre des monuments nationaux ")
            org_name_by_id[oid] = (info.get("name") or "").strip()
        except Exception:
            org_name_by_id[oid] = ""  # si échec, on laisse vide

    for oid in ORG_IDS:
        org_name = org_name_by_id.get(oid, "")

        try:
            if not org_has_at_least_one_dataset(session, oid):
                counts_by_org[oid] = 0
                log(f"⏭️  {oid} ({org_name}) : 0 dataset → ignoré" if org_name else f"⏭️  {oid} : 0 dataset → ignoré")
                skipped += 1
                continue

            df = download_org_csv(session, oid, log)

            # ✅ Ajout du nom d'organisation dans les lignes du catalogue
            df["organization_name"] = org_name

            n = len(df)
            counts_by_org[oid] = n
            log(f"✅ {oid} ({org_name}) : {n} dataset(s)" if org_name else f"✅ {oid} : {n} dataset(s)")

            frames.append(df)

        except Exception as e:
            counts_by_org[oid] = None
            log(f"⚠️ Erreur pour {oid} ({org_name}): {e}" if org_name else f"⚠️ Erreur pour {oid}: {e}")
            failed += 1

    if not frames:
        log("❌ Aucun CSV n’a pu être récupéré.")
        # stats minimal
        pd.DataFrame(
            [{
                "run_utc": run_ts,
                "organization_id": oid,
                "organization_name": org_name_by_id.get(oid, ""),
                "datasets_count": "",
                "status": "error",
            } for oid in ORG_IDS]
        ).to_csv(LOG_STATS_PATH, index=False, encoding="utf-8")
        return 1

    final_df = pd.concat(frames, ignore_index=True)

    # Stabilise les diffs git
    if "id" in final_df.columns:
        # inclut org name pour stabilité si besoin
        sort_cols = ["organization_id", "id"]
        final_df = final_df.sort_values(by=sort_cols, kind="mergesort")

    final_df = sanitize_for_flat_files(final_df)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # Export DINUM attendu en ;
    final_df.to_csv(
        OUT_PATH,
        sep=";",
        index=False,
        encoding="utf-8",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        lineterminator="\n",
    )

    # Export stats structurées
    stats_rows = []
    for oid in ORG_IDS:
        c = counts_by_org.get(oid)
        stats_rows.append(
            {
                "run_utc": run_ts,
                "organization_id": oid,
                "organization_name": org_name_by_id.get(oid, ""),
                "datasets_count": "" if c is None else c,
                "status": "error" if c is None else ("empty" if c == 0 else "ok"),
            }
        )
    pd.DataFrame(stats_rows).to_csv(LOG_STATS_PATH, index=False, encoding="utf-8")

    # Rapport final (log texte)
    log("")
    log("🎉 Export final généré : " + OUT_PATH)
    log("📊 Total lignes : " + str(len(final_df)))
    log(f"ℹ️ Orgs ignorées (0 dataset): {skipped} | échecs: {failed}")
    log("")
    log("📌 Datasets par organisation :")
    for oid in ORG_IDS:
        c = counts_by_org.get(oid)
        name = org_name_by_id.get(oid, "")
        label = f"{oid} ({name})" if name else oid
        if c is None:
            log(f" - {label} : ERREUR")
        else:
            log(f" - {label} : {c}")

    log("")
    log("📄 Fichiers générés :")
    log(" - " + OUT_PATH)
    log(" - " + LOG_TXT_PATH)
    log(" - " + LOG_STATS_PATH)

    return 0


if __name__ == "__main__":
    main()
