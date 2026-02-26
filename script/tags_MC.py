#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import requests

URL = "https://tabular-api.data.gouv.fr/api/resources/4d732341-55cd-43f8-893c-906ed5cfd7fb/data/json/"
OUTPUT_FILE = "tags_ministere_culture.csv"


# Récupération du JSON
response = requests.get(URL, timeout=30)
response.raise_for_status()
data = response.json()


# Calcul des occurrences
tags_dict = {}

for row in data:
    dataset_id = row.get("id")
    tags = row.get("tags")

    if not dataset_id or not tags:
        continue

    for tag in tags.split(","):
        tag = tag.strip()
        if not tag:
            continue

        if tag not in tags_dict:
            tags_dict[tag] = set()

        tags_dict[tag].add(dataset_id)


# Tri des résultats
results = sorted(
    [(tag, len(datasets)) for tag, datasets in tags_dict.items()],
    key=lambda x: (-x[1], x[0])
)


# Export CSV
with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["nom_tag", "nombre_utilisation"])
    writer.writerows(results)


print("Fichier généré :", OUTPUT_FILE)
print("Nombre de tags uniques :", len(results))
