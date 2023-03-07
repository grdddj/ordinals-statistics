from __future__ import annotations

from typing import Iterator

from sqlalchemy import func

from data_db import CollectionModel, InscriptionModel, get_session


def get_document_count() -> int:
    session = get_session()
    return session.query(InscriptionModel).count()


def get_total_content_size() -> int:
    session = get_session()
    return session.query(func.sum(InscriptionModel.content_length)).scalar()


def get_n_biggest_sizes(n: int) -> list[InscriptionModel]:
    session = get_session()
    return (
        session.query(InscriptionModel)
        .order_by(InscriptionModel.content_length.desc())
        .limit(n)
        .all()
    )


def get_n_most_expensive(n: int) -> list[InscriptionModel]:
    session = get_session()
    return (
        session.query(InscriptionModel)
        .order_by(InscriptionModel.genesis_fee.desc())
        .limit(n)
        .all()
    )


def content_types_with_amounts(limit: int) -> list[tuple[str, int]]:
    session = get_session()
    return (
        session.query(InscriptionModel.content_type, func.count(InscriptionModel.id))
        .group_by(InscriptionModel.content_type)
        .order_by(func.count(InscriptionModel.id).desc())
        .limit(limit)
        .all()
    )


def get_duplicate_content_hashes(limit: int) -> list[tuple[str, int]]:
    session = get_session()
    return (
        session.query(InscriptionModel.content_hash, func.count(InscriptionModel.id))
        .group_by(InscriptionModel.content_hash)
        .having(func.count(InscriptionModel.id) > 1)
        .order_by(func.count(InscriptionModel.id).desc())
        .limit(limit)
        .all()
    )


def get_entries_from_content_hash(hash: str, limit: int) -> list[InscriptionModel]:
    session = get_session()
    return (
        session.query(InscriptionModel).filter_by(content_hash=hash).limit(limit).all()
    )


def get_duplicated_content(
    tx_id: str, limit: int = 5
) -> tuple[int, list[InscriptionModel]]:
    session = get_session()
    content_hash = (
        session.query(InscriptionModel.content_hash).filter_by(tx_id=tx_id).first()
    )
    if content_hash is None:
        return 0, []
    else:
        content_hash = content_hash[0]
    amount = (
        session.query(InscriptionModel)
        .filter_by(content_hash=content_hash)
        .filter(InscriptionModel.tx_id != tx_id)
        .count()
    )
    if amount == 0:
        return amount, []
    examples = (
        session.query(InscriptionModel)
        .filter_by(content_hash=content_hash)
        .filter(InscriptionModel.tx_id != tx_id)
        .limit(limit)
        .all()
    )
    return amount, examples


def get_most_active_addresses(limit: int) -> list[tuple[str, int]]:
    session = get_session()
    return (
        session.query(InscriptionModel.minted_address, func.count(InscriptionModel.id))
        .group_by(InscriptionModel.minted_address)
        .order_by(func.count(InscriptionModel.id).desc())
        .limit(limit)
        .all()
    )


def sort_by_timestamp(limit: int) -> list[InscriptionModel]:
    session = get_session()
    return (
        session.query(InscriptionModel)
        .order_by(func.datetime(InscriptionModel.timestamp, "unixepoch").asc())
        .limit(limit)
        .all()
    )


def get_biggest_collections(limit: int) -> list[tuple[CollectionModel, int]]:
    session = get_session()
    return (
        session.query(
            CollectionModel,
            func.count(InscriptionModel.id).label("num_inscriptions"),
        )
        .join(CollectionModel.inscriptions)
        .group_by(CollectionModel.id, CollectionModel.name)
        .order_by(func.count(InscriptionModel.id).desc())
        .limit(limit)
        .all()
    )


def get_collections_using_most_space(limit: int) -> list[tuple[CollectionModel, int]]:
    session = get_session()
    return (
        session.query(
            CollectionModel,
            func.sum(InscriptionModel.content_length).label("total_length"),
        )
        .join(CollectionModel.inscriptions)
        .group_by(CollectionModel.id, CollectionModel.name)
        .order_by(func.sum(InscriptionModel.content_length).desc())
        .limit(limit)
        .all()
    )


def all_inscriptions_from_collection(collection_id: str) -> Iterator[InscriptionModel]:
    session = get_session()
    collection = session.get(CollectionModel, collection_id)
    assert collection is not None
    yield from collection.inscriptions_iter()


if __name__ == "__main__":
    # count = get_document_count()
    # print(count)

    # size = get_total_content_size()
    # print("size", size)

    # biggest = get_n_biggest_sizes(10)
    # for item in biggest:
    #     print(item)

    # content_types = content_types_with_amounts()
    # for c_type, amount in content_types:
    #     print(f"{c_type}: {amount}")

    # duplicates = get_duplicate_content_hashes(25)
    # for hash, amount in duplicates:
    #     examples = get_entries_from_content_hash(hash, 5)
    #     print(f"{hash}: {amount}")
    #     for example in examples:
    #         print(example)

    # addresses = get_most_active_addresses(25)
    # for address, amount in addresses:
    #     print(f"{address}: {amount}")

    # sorted_by_timestamp = sort_by_timestamp(10)
    # for item in sorted_by_timestamp:
    #     print(item)

    # tx_id = "f58ad8178e7fe78624bcd814cf4b655dab8a6d5f293d4a395a8f24c49aaba78a"
    # tx_id = "c734aad65f761e3b3cac88120db17fa1be64242c4a5ef669d5565a08a88a81fa"
    # print(get_duplicated_content(tx_id))

    # collections = get_biggest_collections(10)
    # for collection, num in collections:
    #     print(num, collection)

    # collections = get_collections_using_most_space(10)
    # for collection, num in collections:
    #     print(num, collection)

    for inscr in all_inscriptions_from_collection("xexadons"):
        print(inscr)
