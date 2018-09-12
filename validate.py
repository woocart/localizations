"""Validate that localization files conform to defined schemas."""

from schema import YamlSchema
from strictyaml import StrictYAMLError

import os

# validate country files
for country in os.listdir("Countries"):
    try:
        print(f'Validating {country}/local.yaml" ...')
        YamlSchema.load("Countries", f"{country}/local.yaml", YamlSchema.localization)
    except StrictYAMLError as e:
        print(e)
        print(
            f'!!! Error parsing "{country}/local.yaml". Look above for the reason. !!!'
        )
        exit(1)

# validate template.yaml
try:
    print('Validating "template.yaml" ...')
    YamlSchema.load("./", "template.yaml", YamlSchema.localization)
except StrictYAMLError as e:
    print(e)
    print('!!! Error parsing "template.yaml". Look above for the reason. !!!')
    exit(1)
