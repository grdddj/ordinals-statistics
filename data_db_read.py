from __future__ import annotations

from sqlalchemy import func

from data_db import InscriptionModel, get_query, get_session


def get_document_count() -> int:
    session = get_session()
    return session.query(InscriptionModel).count()


def get_total_content_size() -> int:
    session = get_session()
    return session.query(func.sum(InscriptionModel.content_length)).scalar()


def get_n_biggest_sizes(n: int) -> list[InscriptionModel]:
    query = get_query()
    return query.order_by(InscriptionModel.content_length.desc()).limit(n).all()


def content_types_with_amounts() -> list[tuple[str, int]]:
    session = get_session()
    return (
        session.query(InscriptionModel.content_type, func.count(InscriptionModel.id))
        .group_by(InscriptionModel.content_type)
        .order_by(func.count(InscriptionModel.id).desc())
        .all()
    )


if __name__ == "__main__":
    count = get_document_count()
    print(count)

    size = get_total_content_size()
    print("size", size)

    biggest = get_n_biggest_sizes(10)
    for item in biggest:
        print(item)

    content_types = content_types_with_amounts()
    for c_type, amount in content_types:
        print(f"{c_type}: {amount}")
