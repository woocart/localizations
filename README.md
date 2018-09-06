# WooCart Localizations

This repository contains default setting for a [WooCart](https://woocart.com/) store and specific settings for each country.

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
>WooCart is a WooCommerce hosting service offered by Niteo GmbH that manages our Service hosting and maintenance. For more information on the privacy practices of Niteo, please visit their [Privacy Policy page](https://woocart.com.co/legal/privacy).

- Create a pull request for the changes.

**Demo Products Translations**

- Make a copy of `products-template.yaml` and translate the text.
- Change the price amounts to reflect your local currency.  
- Create a pull request for the changes.
- Continue with other product translations.

## Proposing a change to a localization

[Open a new issue](https://github.com/woocart/localizations/issues) and explain the proposed change in detail, if possible with external sources. 

## Importing

WIP
