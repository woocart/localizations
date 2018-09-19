"""Validate that localization files conform to defined schemas."""

from bs4 import BeautifulSoup as BS
from bs4 import Comment
from pathlib import Path
from schema import WooSchema
from strictyaml import StrictYAMLError


def main():
    """Run the validators."""

    root: Path = Path(__file__).resolve().parent.parent
    valid_htmls = {
        "legal-cookies.html",
        "legal-terms-and-conditions.html",
        "legal-returns-and-refunds.html",
        "legal-privacy-policy.html",
    }

    for country in root.joinpath("Countries").glob("*"):
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
        try:
            print(f'Validating "{locale}" ...')
            WooSchema.load(locale, WooSchema.localization)
        except StrictYAMLError as err:
            print(f"\n\033[91m💥  Error parsing localization {err}. \n\033[0m")
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
