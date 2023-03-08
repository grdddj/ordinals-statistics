import sys
from pathlib import Path

from dominate import document
from dominate.tags import *

from html_elements import (
    biggest_collections,
    biggest_inscriptions,
    bizzare,
    collections_using_most_space,
    content_size,
    content_types,
    document_count,
    duplicated_content,
    most_expensive_inscriptions,
    page_footer,
    page_resources,
    page_title,
)
from logger import logging

HERE = Path(__file__).parent

file_path = HERE / "html_report.html"
css_file = HERE / "html_report.css"


def create_report() -> None:
    # Create a new HTML document
    doc = document(title="Ordinals statistics")

    # Add CSS to the head section
    with doc.head:
        style(css_file.read_text())
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=1")
        link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css",
            integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor",
            crossorigin="anonymous",
        )

    # Add some content to the document
    with doc:
        with div(cls="row"):
            with div():
                page_title()
        with div(cls="container"):
            with div(cls="row"):
                # First column
                with div(cls="col-md-6"):
                    with div():
                        document_count()
                    with div():
                        biggest_inscriptions(10)
                    with div():
                        content_types(10)
                    with div():
                        biggest_collections(10)
                # Second column
                with div(cls="col-md-6"):
                    with div():
                        content_size()
                    with div():
                        most_expensive_inscriptions(10)
                    with div():
                        duplicated_content(10, examples_n=3)
                    with div():
                        collections_using_most_space(10)

        with div(cls="row"):
            with div():
                bizzare()
        hr()
        page_resources()
        hr()
        page_footer()

    # Save the document to a file
    with open(file_path, "w") as f:
        f.write(doc.render())


if __name__ == "__main__":
    logging.info("started create_report")
    try:
        create_report()
    except Exception as e:
        logging.exception(f"Unexpected error in create_report - {e}")
        print("ERROR")
        sys.exit(1)
    logging.info("ending create_report")
