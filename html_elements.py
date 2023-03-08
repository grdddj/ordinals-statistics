from datetime import datetime

from dominate.tags import *

from data_db import InscriptionModel
from data_db_read import (
    content_types_with_amounts,
    get_biggest_collections,
    get_collections_using_most_space,
    get_document_count,
    get_duplicate_content_hashes,
    get_entries_from_content_hash,
    get_n_biggest_sizes,
    get_n_most_expensive,
    get_total_content_size,
)


def page_title() -> None:
    h1("Ordinals statistics")
    p("Obscure statistics about obscure data")


def page_footer() -> None:
    with footer():
        p(f"Data updated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        with p():
            span("Created by ")
            a("grdddj", href="https://github.com/grdddj", target="_blank")
            span(" in cooperation with ")
            a("ChatGPT", href="https://chat.openai.com/chat", target="_blank")
        with p():
            span("Feel free to")
            a(
                " create an issue ",
                href="https://github.com/grdddj/ordinals-statistics/issues/new",
                target="_blank",
            )
            span("on Github")


def page_resources() -> None:
    h3("Useful resources")
    with p():
        a(
            "Dune.com - dashboard",
            href="https://dune.com/dgtl_assets/bitcoin-ordinals-analysis",
            target="_blank",
        )
    with p():
        a(
            "Dune.com - dashboard",
            href="https://dune.com/domo/ordinals-marketplaces",
            target="_blank",
        )
    with p():
        a(
            "Github.com - ord repository",
            href="https://github.com/casey/ord",
            target="_blank",
        )
    with p():
        a("Ordinals.com - explorer", href="https://ordinals.com/", target="_blank")
    with p():
        a("Ordinals.com - docs", href="https://docs.ordinals.com/", target="_blank")
    with p():
        a(
            "Ordinalswallet.com - explorer",
            href="https://ordinalswallet.com/inscriptions",
            target="_blank",
        )
    with p():
        a(
            "Ordinalswallet.com - collections",
            href="https://ordinalswallet.com/collections",
            target="_blank",
        )
    with p():
        a("Ordswap.io - marketplace", href="https://ordswap.io/", target="_blank")
    with p():
        a("Openordex.org - marketplace", href="https://openordex.org/", target="_blank")
    with p():
        a("Ordx.io - marketplace", href="https://beta.ordx.io/", target="_blank")
    with p():
        a(
            "Pourteaux.xyz - article",
            href="https://read.pourteaux.xyz/p/illegitimate-bitcoin-transactions",
            target="_blank",
        )


def document_count() -> None:
    doc_count = get_document_count()
    h3("Ordinals count")
    p(f"Total number of documents: {doc_count:,}")


def biggest_inscriptions(n: int) -> None:
    biggest = get_n_biggest_sizes(n)
    h3("Biggest inscriptions")
    with table(cls="table"):
        with thead():
            with tr(cls="table-light"):
                th("ID")
                th("TX")
                th("Size [bytes]")
                th("Type")
                th("Date")
                th("Fee [sats]")
        with tbody():
            for entry in biggest:
                with tr():
                    td(a(entry.id, href=entry.ordinals_com_link(), target="_blank"))
                    td(
                        a(
                            entry.tx_id_ellipsis(),
                            href=entry.mempool_space_link(),
                            target="_blank",
                        )
                    )
                    td(f"{entry.content_length:,}")
                    td(entry.content_type)
                    td(entry.datetime.split()[0])
                    td(f"{entry.genesis_fee:,}")


def most_expensive_inscriptions(n: int) -> None:
    biggest = get_n_most_expensive(n)
    h3("Most expensive inscriptions")
    with table(cls="table"):
        with thead():
            with tr(cls="table-light"):
                th("ID")
                th("TX")
                th("Fee [sats]")
                th("Type")
                th("Date")
                th("Size [bytes]")
        with tbody():
            for entry in biggest:
                with tr():
                    td(a(entry.id, href=entry.ordinals_com_link(), target="_blank"))
                    td(
                        a(
                            entry.tx_id_ellipsis(),
                            href=entry.mempool_space_link(),
                            target="_blank",
                        )
                    )
                    td(f"{entry.genesis_fee:,}")
                    td(entry.content_type.split(";")[0])
                    td(entry.datetime.split()[0])
                    td(f"{entry.content_length:,}")


def content_types(n: int) -> None:
    content_type_amounts = content_types_with_amounts(n)
    h3("Most common content types")
    with table():
        with thead():
            with tr():
                th("Type")
                th("Amount")
        with tbody():
            for content_type, amount in content_type_amounts:
                with tr():
                    td(content_type.split(";")[0])
                    td(f"{amount:,}")


def content_size() -> None:
    content_size_bytes = get_total_content_size()
    mb_size = int(content_size_bytes / 1024 / 1024)
    h3("Total size")
    p(f"Total size of documents (without transaction data): {mb_size:,} MB")


def duplicated_content(n: int, examples_n: int) -> None:
    most_duplicated_content = get_duplicate_content_hashes(n)
    h3("Most duplicated content")
    with table():
        with thead():
            with tr():
                th("Amount")
                th("Content type")
                th("Content length")
                th("Examples")
        with tbody():
            for hash, amount in most_duplicated_content:
                examples = get_entries_from_content_hash(hash, examples_n)
                content_type = examples[0].content_type
                content_length = examples[0].content_length
                with tr():
                    td(f"{amount:,}")
                    td(content_type.split(";")[0])
                    td(f"{content_length:,}")
                    td(
                        *[
                            a(
                                example.id,
                                href=example.ordinals_com_link(),
                                target="_blank",
                            )
                            for example in examples
                        ]
                    )


def collections_using_most_space(n: int) -> None:
    collections = get_collections_using_most_space(n)
    h3("Collections using most space")
    with table():
        with thead():
            with tr():
                th("ID")
                th("Used space [bytes]")
                th("Amount")
                th("Description")
        with tbody():
            for collection, used_space in collections:
                with tr():
                    td(
                        a(
                            collection.id,
                            href=collection.link_ordinalswallet(),
                            target="_blank",
                        )
                    )
                    td(f"{used_space:,}")
                    td(f"{int(collection.supply):,}")
                    td(collection.description)


def biggest_collections(n: int) -> None:
    collections = get_biggest_collections(n)
    h3("Biggest collections")
    with table():
        with thead():
            with tr():
                th("ID")
                th("Amount")
                th("Description")
        with tbody():
            for collection, amount in collections:
                with tr():
                    td(
                        a(
                            collection.id,
                            href=collection.link_ordinalswallet(),
                            target="_blank",
                        )
                    )
                    td(f"{amount:,}")
                    td(collection.description)


def bizzare() -> None:
    tx_ids_descriptions = [
        (
            "6a415863875f212082dc78d96d27565e97fbc6f1f16a11a5e6dc9850cf6e8d00i0",
            "Whole fckin HTML website",
        ),
        (
            "0fa05780d91262c22d5b62a4fbebfa5dbed8fbf1e5b169346830ac99d9cebf70i0",
            "PDF with a dishwasher (and maybe a virus)",
        ),
        (
            "c86d37524b435a440a668f9b2eba85fdad084f451f44950c0650dc2976fd965bi0",
            "Holy bible on the blockchain",
        ),
        (
            "220e3a7f6c190042194302c0037ac4fa42894d9c87152e7809bb340b1c5dcc02i0",
            "ETH whitepaper",
        ),
        ("5e92195849607b400d77f01cb1146563ce523fed47f66a044e7a470016e05e59i0", "Fart"),
        (
            "55a06c90671f1f3a30fe1b49a4fb1b606eebb10c842e29562214d786a645f8dci0",
            "BTC whitepaper",
        ),
        (
            "db5fa1f5ab30cad822ce0b28a5751617fc1e7cdf07457d2910f9d1bad511d708i0",
            "Wanna play some music?",
        ),
        ("521f8eccffa4c41a3a7728dd012ea5a4a02feed81f41159231251ecf1e5c79dai0", "DOOM"),
    ]

    h3("Bizzare")
    with table():
        with thead():
            with tr():
                th("ID")
                th("Description")
                th("Date")
                th("Size [bytes]")
        with tbody():
            for tx_id, description in tx_ids_descriptions:
                if len(tx_id) == 66:
                    tx_id = tx_id[:64]
                inscription = InscriptionModel.by_tx_id(tx_id)
                with tr():
                    td(
                        a(
                            inscription.id,
                            href=inscription.ordinals_com_content_link(),
                            target="_blank",
                        )
                    )
                    td(description)
                    td(inscription.datetime.split()[0])
                    td(f"{inscription.content_length:,}")
