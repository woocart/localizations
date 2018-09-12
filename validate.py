"""Validate that localization files conform to defined schemas."""

from schema import YamlSchema

# validate template.yaml
schema = YamlSchema.load("./", "template.yaml", YamlSchema.localization)
