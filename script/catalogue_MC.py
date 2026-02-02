#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from io import StringIO

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


# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------
def org_has_at_least_one_dataset(session: requests.Session, oid: str) -> bool:
    """Teste si l'organisation a au moins 1 dataset via l'API JSON (pas de pagination nécessaire)."""
    url = f"https://www.data.gouv.fr/api/1/organizations/{oid}/datasets/?page_size=1"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    payload = r.json()
    return bool(payload.get("data"))


def download_org_csv(session: requests.Session, oid: str) -> pd.DataFrame:
    """Télécharge le CSV datasets.csv pour une organisation et le charge en DataFrame."""
    url = f"https://www.data.gouv.fr/api/1/organizations/{oid}/datasets.csv"
    print(f"📥 Téléchargement : {url}")

    r = session.get(url, timeout=60)
    r.raise_for_status()

    # CSV data.gouv : généralement séparateur ';' + quotechar '"'
    df = pd.read_csv(
        StringIO(r.text),
        sep=";",
        quotechar='"',
        engine="python",
        on_bad_lines="warn",  # tolérant en cas de ligne tordue
    )
    df["organization_id"] = oid
    return df


def sanitize_for_github_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Évite l'erreur GitHub 'Illegal quoting' en supprimant les retours à la ligne
    à l'intérieur des champs texte (description, etc.).
    """
    obj_cols = df.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        # Remplace CR/LF internes par un espace
        df[c] = df[c].astype(str).str.replace(r"[\r\n]+", " ", regex=True)
    return df


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------
def main() -> int:
    session = requests.Session()

    frames = []
    counts_by_org = {}
    skipped = 0
    failed = 0

    for oid in ORG_IDS:
        try:
            if not org_has_at_least_one_dataset(session, oid):
                counts_by_org[oid] = 0
                print(f"⏭️  {oid} : 0 dataset → ignoré")
                skipped += 1
                continue

            df = download_org_csv(session, oid)
            n = len(df)
            counts_by_org[oid] = n
            print(f"✅ {oid} : {n} dataset(s)")

            frames.append(df)

        except Exception as e:
            counts_by_org[oid] = None
            print(f"⚠️ Erreur pour {oid}: {e}")
            failed += 1

    if not frames:
        print("❌ Aucun CSV n’a pu être récupéré (ou toutes les orgs sont vides).")
        return 1

    final_df = pd.concat(frames, ignore_index=True)

    # (Optionnel) tri pour stabiliser les diffs git
    if "id" in final_df.columns:
        final_df = final_df.sort_values(by=["organization_id", "id"], kind="mergesort")

    # ✅ Correction GitHub: enlever retours à la ligne internes
    final_df = sanitize_for_github_csv(final_df)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # ✅ Export stable pour GitHub (quoting + lineterminator)
    final_df.to_csv(
        OUT_PATH,
        sep=";",
        index=False,
        encoding="utf-8",
        quotechar='"',
        quoting=csv.QUOTE_ALL,
        lineterminator="\n",
    )

    print("\n🎉 Export final généré :", OUT_PATH)
    print("📊 Total lignes :", len(final_df))
    print(f"ℹ️ Orgs ignorées (0 dataset): {skipped} | échecs: {failed}")

    print("\n📌 Datasets par organisation :")
    for oid in ORG_IDS:
        c = counts_by_org.get(oid)
        if c is None:
            print(f" - {oid} : ERREUR")
        else:
            print(f" - {oid} : {c}")

    return 0


if __name__ == "__main__":
    main()
