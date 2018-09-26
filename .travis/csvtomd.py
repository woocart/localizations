"""Convert CSV to HTML file."""

from os import getcwd
from pathlib import Path

import csv
import urllib.request

t = """\
<!--
title: {name}
description: |+
  {short}
stock: instock
price: {price}
images:
{images}
-->
{long}
"""


def parse(csv_file: str, base: str):
    """Parse CSV and output HTML file with base name.

    Arguments:
        csv_file {str} -- Path to the csv file.
        base {str} -- Name of the base HTML file and folder with images.
    """

    products = []
    with open(csv_file) as csvfile:
        out = csv.reader(csvfile, delimiter=",", quotechar='"')
        c = 0
        for row in out:
            if c == 0:
                c += 1
                continue
            c += 1
            name, long, short, price, images = row
            links = []
            for image in images.split(", "):
                stem = Path(image.replace("https://", "/")).name
                local = Path(getcwd()).joinpath(base)
                Path(local).mkdir(exist_ok=True)
                local = local.joinpath(stem)
                if not Path(local).exists():
                    urllib.request.urlretrieve(image, local)
                links.append(f"  - common:{base}/{stem}")
            images = "\n".join(links)
            products.append(
                t.format(
                    name=name,
                    short=short.replace("\n", "\n  "),
                    long=long,
                    price=price,
                    images=images,
                )
            )
    Path(getcwd()).joinpath(f"{base}.html").write_text("---\n".join(products))


parse("electronics.csv", "electronics")
parse("bookstore.csv", "bookstore")
parse("toys.csv", "toys")
parse("jewellery.csv", "jewellery")
