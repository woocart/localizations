"""Schemas for YAML localization files."""

from const import COUNTRIES
from const import CURRENCIES
from const import TIMEZONES
from pathlib import Path
from strictyaml import Any
from strictyaml import as_document
from strictyaml import Bool
from strictyaml import Decimal
from strictyaml import Enum
from strictyaml import Int
from strictyaml import load as yaml_load
from strictyaml import Map
from strictyaml import MapPattern
from strictyaml import Optional
from strictyaml import Seq
from strictyaml import Str
from strictyaml import YAMLError
from wplang import WPLANGS

import copy


class WooSchema:
    """Schema for localization YAML files."""

    # https://github.com/woocart/woocart-defaults/blob/master/src/importers/class-woopage.php#L14
    productMeta = {
        "title": Str(),
        "description": Str(),
        Optional("price"): Str(),
        Optional("category"): Str(),
        "images": Seq(Str()),
    }

    # https://github.com/woocart/woocart-defaults/blob/master/src/importers/class-woopage.php#L14
    pageMeta = {
        "post_title": Str(),
        Optional("post_name"): Str(),
        Optional("post_excerpt"): Str(),
        "post_status": Enum(["draft", "publish"]),
        "post_type": Enum(["page", "post"]),
        Optional("post_category"): Str(),
        Optional("meta_input"): MapPattern(Str(), Str()),
        Optional("woocart_defaults"): MapPattern(Str(), Str()),
    }

    localization = {
        "woo/woocommerce_default_country": Enum(COUNTRIES),
        "wp/date_format": Enum(["d/m/Y", "Y-m-d", "F j, Y", "m/d/Y"]),
        "wp/time_format": Enum(["H:i", "g:i A"]),
        "wp/start_of_week": Enum(["1", "2", "3", "4", "5", "6", "7"]),
        "wp/timezone_string": Enum(TIMEZONES),
        "wp/blog_charset": Enum(["UTF-8"]),
        "wp/DEFAULT_WPLANG": Enum(WPLANGS),
        Optional("wp/blogdescription"): Str(),
        Optional("wp/woocommerce_demo_store_notice"): Str(),
        "woo/woocommerce_weight_unit": Enum(["kg", "k", "lbs", "oz"]),
        "woo/woocommerce_dimension_unit": Enum(["m", "cm", "mm", "in", "yd"]),
        "woo/woocommerce_currency": Enum(CURRENCIES),
        "woo/woocommerce_currency_pos": Enum(
            ["right_space", "left_space", "left", "right"]
        ),
        "woo/woocommerce_price_thousand_sep": Enum([".", ","]),
        "woo/woocommerce_price_decimal_sep": Enum([",", "."]),
        "woo/woocommerce_price_num_decimals": Enum(["2"]),
        Optional("woo/woocommerce_tax_classes"): Seq(Str()),
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
        ".woo/woocommerce_bacs_settings_format": Enum(["serialized"]),
        ".woo/woocommerce_cod_settings_format": Enum(["serialized"]),
        Optional(".woo/woocommerce_tax_classes_format"): Enum(["implode_newline"]),
    }

    @staticmethod
    def load(path: Path, schema_pointer):
        """Load and validate .yaml file."""
        schema = copy.deepcopy(schema_pointer)
        with path.open() as f:
            yaml = f.read()
            data = yaml_load(yaml, Any())
            is_template = path.name == "template.yaml"

            # Replace real Country and Timezone values with fakes
            if is_template:
                schema["woo/woocommerce_default_country"] = Enum(["LL"])
                schema["wp/timezone_string"] = Enum(["Region/Country"])
                schema["wp/DEFAULT_WPLANG"] = Enum(["ll_LL"])
                schema["woo/woocommerce_currency"] = Enum(["LLL"])

            if "woo/woocommerce_tax_classes" in data:
                # Inspect that tax classes and taxes match

                # create enum for taxes from defined tax_classes
                tax_classes = [
                    str(tax).lower().replace(" ", "-")
                    for tax in data["woo/woocommerce_tax_classes"]
                ]
                # +1 is for standard schema which is never defined in tax class
                for x in range(len(tax_classes) + 1):
                    # start counting with 1
                    schema[f"wootax/{x+1}"] = Map(
                        {
                            "country": Enum(["LL"]) if is_template else Enum(COUNTRIES),
                            "state": Str(),
                            "rate": Decimal(),
                            "name": Str(),
                            "priority": Int(),
                            "compound": Int(),
                            "shipping": Int(),
                            "order": Int(),
                            "class": Enum([""]) if x == 0 else Enum(tax_classes),
                            "locations": Map({}),
                        }
                    )
            try:
                return yaml_load(yaml, Map(schema), path)
            except YAMLError:
                raise

        return as_document(schema)

    @staticmethod
    def load_string(data: bytes, schema, path: str):
        """Load and validate yaml data."""
        try:
            return yaml_load(data, Map(schema), path)
        except YAMLError:
            raise

        return as_document(schema)
