from datetime import datetime
from pathlib import Path

from dominate import document
from dominate.tags import *

from data_db_read import (
    content_types_with_amounts,
    get_document_count,
    get_duplicate_content_hashes,
    get_entries_from_content_hash,
    get_n_biggest_sizes,
    get_total_content_size,
)

HERE = Path(__file__).parent

file_path = HERE / "report.html"

# Create a new HTML document
doc = document(title="Ordinals statistics")

# Add some content to the document
with doc:
    with div():
        h1("Ordinals statistics")
    with div():
        doc_count = get_document_count()
        h3("Ordinals count")
        p(f"Total number of documents: {doc_count}")
    with div():
        content_size_bytes = get_total_content_size()
        mb_size = int(content_size_bytes / 1024 / 1024)
        h3("Total size")
        p(f"Total size of documents (without transaction data): {mb_size} MB")
    with div():
        ten_biggest = get_n_biggest_sizes(10)
        h3("10 biggest inscriptions")
        with table():
            with thead():
                with tr():
                    th("ID")
                    th("TX")
                    th("length [bytes]")
                    th("type")
                    th("date")
                    th("fee [sats]")
            with tbody():
                for entry in ten_biggest:
                    with tr():
                        td(a(entry.id, href=entry.ordinals_com_link(), target="_blank"))
                        td(
                            a(
                                entry.tx_id_ellipsis(),
                                href=entry.mempool_space_link(),
                                target="_blank",
                            )
                        )
                        td(entry.content_length)
                        td(entry.content_type)
                        td(entry.datetime.split()[0])
                        td(entry.genesis_fee)
    with div():
        content_type_amounts = content_types_with_amounts()
        h3("Content type amounts")
        with table():
            with thead():
                with tr():
                    th("Type")
                    th("Amount")
            with tbody():
                for content_type, amount in content_type_amounts:
                    with tr():
                        td(content_type)
                        td(amount)
    with div():
        most_duplicated_content = get_duplicate_content_hashes(10)
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
                    examples = get_entries_from_content_hash(hash, 5)
                    content_type = examples[0].content_type
                    content_length = examples[0].content_length
                    with tr():
                        td(amount)
                        td(content_type)
                        td(content_length)
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

    hr()

    h3("Some resources")
    with p():
        a("Dune.com - dashboard", href="https://dune.com/dgtl_assets/bitcoin-ordinals-analysis", target="_blank")
    with p():
        a("Dune.com - dashboard", href="https://dune.com/domo/ordinals-marketplaces", target="_blank")
    with p():
        a("Github.com - ord repository", href="https://github.com/casey/ord", target="_blank")
    with p():
        a("Ordinals.com - explorer", href="https://ordinals.com/", target="_blank")
    with p():
        a("Ordinals.com - docs", href="https://docs.ordinals.com/", target="_blank")
    with p():
        a("Ordinalswallet.com - explorer", href="https://ordinalswallet.com/inscriptions", target="_blank")
    with p():
        a("Ordinalswallet.com - collections", href="https://ordinalswallet.com/collections", target="_blank")
    with p():
        a("Ordswap.io - marketplace", href="https://ordswap.io/", target="_blank")
    with p():
        a("Openordex.org - marketplace", href="https://openordex.org/", target="_blank")
    with p():
        a("Ordx.io - marketplace", href="https://beta.ordx.io/", target="_blank")
    with p():
        a("Pourteaux.xyz - article", href="https://read.pourteaux.xyz/p/illegitimate-bitcoin-transactions", target="_blank")

    hr()

    p(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with p():
        span("Created by ")
        a("grdddj", href="https://github.com/grdddj", target="_blank")

# Save the document to a file
with open(file_path, "w") as f:
    f.write(doc.render())
