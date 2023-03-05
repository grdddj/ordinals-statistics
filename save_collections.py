from __future__ import annotations

import json
from typing import Any

from common import ORDINALS_COLLECTIONS_DIR
from data_db import CollectionModel, InscriptionModel, get_session

collections = {}

session = get_session()

for dirpath in ORDINALS_COLLECTIONS_DIR.iterdir():
    if dirpath.is_dir():
        print(dirpath)
        inscriptions_file = dirpath / "inscriptions.json"
        meta_file = dirpath / "meta.json"
        with open(meta_file) as f:
            meta_data: dict[str, str] = json.load(f)
            name = meta_data["name"]
            inscription_icon = meta_data["inscription_icon"]
            supply = meta_data["supply"]
            slug = meta_data["slug"]
            description = meta_data["description"]
            twitter_link = meta_data["twitter_link"]
            discord_link = meta_data["discord_link"]
            website_link = meta_data["website_link"]
            new_collection = CollectionModel(
                id=slug,
                name=name,
                inscription_icon=inscription_icon,
                supply=supply,
                slug=slug,
                description=description,
                twitter_link=twitter_link,
                discord_link=discord_link,
                website_link=website_link,
            )

            with open(inscriptions_file) as f:
                inscriptions: list[dict[str, Any]] = json.load(f)
                all_ordinals: list[InscriptionModel] = []
                for inscr in inscriptions:
                    id = inscr["id"]
                    name = inscr["meta"].get("name", "")
                    tx_id = id[:64]

                    ordinal = (
                        session.query(InscriptionModel)
                        .filter(InscriptionModel.tx_id == tx_id)
                        .first()
                    )
                    if ordinal is None:
                        # print(f"Ordinal {tx_id} not found in database")
                        continue
                    ordinal.name_from_collection = name
                    all_ordinals.append(ordinal)

            new_collection.inscriptions = all_ordinals
            session.add(new_collection)

session.commit()
session.close()
