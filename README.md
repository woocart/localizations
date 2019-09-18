[![WooCart Project](https://img.shields.io/badge/powered%20by-WooCart-943af9.svg)](https://woocart.com) [![Build Status](https://travis-ci.com/woocart/localizations.svg?branch=master)](https://travis-ci.com/woocart/localizations)
# WooCart Localizations

This repository contains default settings for a [WooCart](https://woocart.com/) store and specific settings for each country.

## Making a new localization

There are three types of localization: store (WordPress and WooCommerce settings), legal pages (privacy, terms, need to be GDPR compliant) and demo products translations.

**Store Localization**

- Make a copy `template.yaml` and change the values for your country.
- Name file with the short code of your country `Country/local.yaml`.
- Create a pull request for the changes.

**Legal Pages**

- The minimum is three legal pages - Privacy Policy, Terms and Conditions, and Returns and Refunds.
- Create the legal pages that reflect your local laws. Make sure that they are GDPR compliant and refer to WooCart as one of the third-party service providers. Here is a template:

>WooCart Hosting
>
>WooCart is a WooCommerce hosting service offered by Niteo GmbH that manages our Service hosting and maintenance. For more information on the privacy practices of Niteo, please visit their [Privacy Policy page](https://woocart.com/legal/privacy).

- Create a pull request for the changes.

**Demo Products Translations**

- Make a copy of `products-template.yaml` and translate the text.
- Change the price amounts to reflect your local currency.
- Create a pull request for the changes.
- Continue with other product translations.

## Proposing a change to a localization

[Open a new issue](https://github.com/woocart/localizations/issues) and explain the proposed change in detail, if possible with external sources.


## Supported WordPress shortcodes

- `[woo-include page="SOME-NAME"]` - Inlines content from page with slug `SOME-NAME`
- `[woo-include post="SOME-NAME"]` - Inlines content from post with slug `SOME-NAME`
- `[company-name]` - Displays company name
- `[tax-id]` - Displays tax id
- `[policy-page]` - Displays HTML A element with link to the policy page
- `[store-url]` - Displays HTML A element with link to the store page
- `[store-name]` - Displays store name
- `[cookie-page]` - Displays HTML A element with link to the cookie page
- `[returns-page]` - Displays HTML A element with link to the returns & refunds page
- `[terms-page]` - Displays HTML A element with link to the terms & conditions page
- `[contact-page]` - Displays HTML A element with link to the contact us page
- `[woo-permalink]` - Displays HTML A element with link to the page for which the `page_id` is provided as an argument
- `[woocart]` - Display HTML A element with a link to [https://woocart.com](https://woocart.com) and `WooCart` as text 

### Usage
- Default: `[woo-permalink option="page_id"]`
- Custom content: `[woo-permalink option="page_id"]<a href="%s">Some text</a>[/woo-permalink]`


## Exporting products from WooCommerce

- Go to `Products` > `Export`
- Select `Name`, `Description`, `Short Description`, `Regular Price`, `Images` in the export field.
- Save file to `csv` folder
- Run `pipenv run python .travis/csv2html.py csv/your_file_name.csv Countries/.common/store_name` to generate product HTML page and download images for products.

## Translating the products

- Copy the products HTML you want to translate to the Country folder
- Edit the `title`, `description` and body fields.

Both HTML and Markdown are supported for the body of the product.
