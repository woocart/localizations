"""Schemas for YAML localization files."""

from const import COUNTRIES
from const import CURRENCIES
from const import TIMEZONES
from const import WPLANGS
from strictyaml import as_document
from strictyaml import Bool
from strictyaml import Decimal
from strictyaml import Enum
from strictyaml import Int
from strictyaml import load as yaml_load
from strictyaml import Map
from strictyaml import Optional
from strictyaml import Str
from strictyaml import YAMLError

import os


class YamlSchema:
    """Schema for localization YAML files."""

    localization = {
        "woo/woocommerce_default_country": Enum(COUNTRIES),
        "wp/date_format": Enum(["d/m/Y", "Y-m-d", "F j, Y", "m/d/Y"]),
        "wp/time_format": Enum(["H:i", "g:i A"]),
        "wp/start_of_week": Enum(["1", "2", "3", "4", "5", "6", "7"]),
        "wp/timezone_string": Enum(TIMEZONES),
        "wp/blog_charset": Enum(["UTF-8"]),
        "wp/WPLANG": Enum(WPLANGS),
        "woo/woocommerce_weight_unit": Enum(["kg", "k", "lbs", "oz"]),
        "woo/woocommerce_dimension_unit": Enum(["m", "cm", "mm", "in", "yd"]),
        "woo/woocommerce_currency": Enum(CURRENCIES),
        "woo/woocommerce_currency_pos": Enum(
            ["right_space", "left_space", "left", "right"]
        ),
        "woo/woocommerce_price_thousand_sep": Enum([".", ","]),
        "woo/woocommerce_price_decimal_sep": Enum([",", "."]),
        "woo/woocommerce_price_num_decimals": Enum(["2"]),
        "woo/woocommerce_tax_classes": Str(),
        Optional("wootax/1"): Map(
            {
                "country": Enum(COUNTRIES),
                "state": Str(),
                "rate": Decimal(),
                "name": Str(),
                "priority": Int(),
                "compound": Int(),
                "shipping": Int(),
                "order": Int(),
                "class": Str(),
                "locations": Map({}),
            }
        ),
        Optional("wootax/2"): Map(
            {
                "country": Enum(COUNTRIES),
                "state": Str(),
                "rate": Decimal(),
                "name": Str(),
                "priority": Int(),
                "compound": Int(),
                "shipping": Int(),
                "order": Int(),
                "class": Str(),
                "locations": Map({}),
            }
        ),
        Optional("wootax/3"): Map(
            {
                "country": Enum(COUNTRIES),
                "state": Str(),
                "rate": Decimal(),
                "name": Str(),
                "priority": Int(),
                "compound": Int(),
                "shipping": Int(),
                "order": Int(),
                "class": Str(),
                "locations": Map({}),
            }
        ),
        Optional("wootax/4"): Map(
            {
                "country": Enum(COUNTRIES),
                "state": Str(),
                "rate": Decimal(),
                "name": Str(),
                "priority": Int(),
                "compound": Int(),
                "shipping": Int(),
                "order": Int(),
                "class": Str(),
                "locations": Map({}),
            }
        ),
        Optional("wootax/5"): Map(
            {
                "country": Enum(COUNTRIES),
                "state": Str(),
                "rate": Decimal(),
                "name": Str(),
                "priority": Int(),
                "compound": Int(),
                "shipping": Int(),
                "order": Int(),
                "class": Str(),
                "locations": Map({}),
            }
        ),
        "woo/woocommerce_bacs_settings": Map(
            {
                "enabled": Bool(),
                Optional("title"): Str(),
                Optional("description"): Str(),
                Optional("instructions"): Str(),
                Optional("account_name"): Str(),
                Optional("account_number"): Str(),
                Optional("sort_code"): Str(),
                Optional("bank_name"): Str(),
                Optional("iban"): Str(),
                Optional("bic"): Str(),
                Optional("account_details"): Str(),
            }
        ),
        "woo/woocommerce_cod_settings": Map(
            {
                "enabled": Bool(),
                Optional("title"): Str(),
                Optional("description"): Str(),
                Optional("instructions"): Str(),
                Optional("enable_for_methods"): Str(),
                Optional("enable_for_virtual"): Bool(),
            }
        ),
        "woo/woocommerce_checkout_privacy_policy_text": Str(),
        "woo/woocommerce_registration_privacy_policy_text": Str(),
    }

    def load(folder, file, schema):
        """Load and validate .yaml file."""
        with open(os.path.join(folder, file)) as f:

            # Replace real Country and Timezone values with fakes
            if file == "template.yaml":
                schema["woo/woocommerce_default_country"] = Enum(["LL"])
                schema["wp/timezone_string"] = Enum(["Region/Country"])
                schema["wp/WPLANG"] = Enum(["ll_LL"])
                schema["woo/woocommerce_currency"] = Enum(["LLL"])

                for key in schema.keys():
                    if str(key) == 'Optional("wootax/1")':
                        dict_subschema = schema[key]._validator_dict
                        dict_subschema["country"] = Enum(["LL"])
                        schema[key] = Map(dict_subschema)
                    if str(key) == 'Optional("wootax/2")':
                        dict_subschema = schema[key]._validator_dict
                        dict_subschema["country"] = Enum(["LL"])
                        schema[key] = Map(dict_subschema)
                    if str(key) == 'Optional("wootax/3")':
                        dict_subschema = schema[key]._validator_dict
                        dict_subschema["country"] = Enum(["LL"])
                        schema[key] = Map(dict_subschema)

            try:
                return yaml_load(f.read(), Map(schema))
            except YAMLError:
                raise

        return as_document(schema)
