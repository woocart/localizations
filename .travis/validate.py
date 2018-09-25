"""Validate that localization files conform to defined schemas."""

from bs4 import BeautifulSoup as BS
from bs4 import Comment
from pathlib import Path
from schema import WooSchema
from strictyaml import StrictYAMLError

import subprocess


def main():
    """Run the validators."""

    root: Path = Path(__file__).resolve().parent.parent
    valid_htmls = {
        "cookies-table.html",
        "legal-cookies.html",
        "legal-terms-and-conditions.html",
        "legal-returns-and-refunds.html",
        "legal-privacy-policy.html",
    }

    for country in root.joinpath("Countries").glob("*"):
        if str(country.stem).startswith("."):
            continue
        print(f'\nInspecting "{country.stem}" ...')
        htmls = []
        # validate html files
        for html in country.glob("*.html"):
            htmls.append(html.name)
            try:
                print(f'Validating "{html}" ...')
                soup = BS(html.read_text(), "html.parser")
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                if not len(comments):
                    print(
                        f"\n\033[91m💥  Error parsing {html}. Page meta was not found \n\033[0m"
                    )
                    exit(255)
                WooSchema.load_string(str(comments[0]), WooSchema.pageMeta, html)
            except StrictYAMLError as err:
                print(f"\n\033[91m💥  Error parsing localization {err}. \n\033[0m")
                exit(255)

        if len(htmls) and any(x not in valid_htmls for x in htmls):
            print(
                f"\n\033[91m💥  List of detected HTML files '{','.join(htmls)}' and Expected '{','.join(valid_htmls)}' does not match. \n\033[0m"
            )
            exit(255)

        # validate country file
        locale = country.joinpath("local.yaml")
        language = "en"
        try:
            print(f'Validating "{locale}" ...')
            schema = WooSchema.load(locale, WooSchema.localization)
            language = str(schema["wp/WPLANG"]).split("_")[0]
        except StrictYAMLError as err:
            print(f"\n\033[91m💥  Error parsing localization {err}. \n\033[0m")
            exit(255)

        # spellcheck
        if language in ["en", "ro", "sl"]:
            for html in country.glob("*.html"):
                cat = subprocess.Popen(("cat", html), stdout=subprocess.PIPE)
                english = subprocess.Popen(
                    (
                        "aspell --lang=en --encoding=utf-8 "
                        "--personal=./.travis/dictionaries/en.pws list"
                    ).split(" "),
                    stdin=cat.stdout,
                    stdout=subprocess.PIPE,
                )
                output = subprocess.check_output(
                    (
                        f"aspell --lang={language} --encoding=utf-8 "
                        f"--personal=./.travis/dictionaries/{language}.pws list"
                    ).split(" "),
                    stdin=english.stdout,
                )
                if output:
                    print(
                        f"\n\033[91m💥  Found spelling mistakes in {country.name}/{html.name}: \n{output.decode()}\033[0m"
                    )
                    exit(255)

    # validate template.yaml
    try:
        template = root.joinpath("template.yaml")
        print(f'Validating "{template}" ...')
        WooSchema.load(template, WooSchema.localization)
    except StrictYAMLError as err:
        print(f"\n\033[91m💥  Error parsing localization {err}.\n\033[0m")
        exit(255)

    print("All done! ✨ ✨ ✨")


if __name__ == "__main__":
    main()
