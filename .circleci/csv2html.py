"""Convert CSV from WooCommerce to HTML file.

For example: `.circleci/csv2html.py csv/electronics.csv electronics`
"""

from os import getcwd
from pathlib import Path
from random import randrange

import argparse
import csv
import urllib.request

t = """\
<!--
title: {name}
description: |+
  {short}
price: {price}
images:
{images}
-->
{long}
"""


def main(csv_file: str, base: str):
    """Parse CSV and output HTML file with base name.

    Arguments:
        csv_file: Path to the csv file.
        base: Name of the base HTML file and folder with images.

    """
    products = []
    with open(csv_file) as csvfile:
        out = csv.reader(csvfile, delimiter=",", quotechar='"')
        for i, row in enumerate(out):
            if i == 0:
                continue
            name, long, short, price, images = row
            if not price:
                price = str(randrange(10, 100))
            links = []
            for image in images.split(", "):
                stem = Path(image.replace("https://", "/")).name
                local = Path(getcwd()).joinpath(base)
                Path(local).mkdir(exist_ok=True)
                local = local.joinpath(stem)
                if not Path(local).exists():
                    urllib.request.urlretrieve(image, local)
                common = base.replace("Countries/.common/", "common:")
                links.append(f"  - {common}/{stem}")
            images = "\n".join(links)
            products.append(
                t.format(
                    name=name,
                    short=short.replace("\n", "\n  "),
                    long=long.replace(" 	", "  "),
                    price=price,
                    images=images,
                )
            )
    Path(getcwd()).joinpath(f"{base}.html").write_text("---\n".join(products))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog=__doc__)
    parser.add_argument("csv_file", type=str, help="path to csv file")
    parser.add_argument(
        "base", type=str, help="name of the output html and folder for images"
    )
    args = parser.parse_args()
    main(**vars(args))
