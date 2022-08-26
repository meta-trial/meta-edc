from edc_identifier.simple_identifier import (
    SimpleTimestampIdentifier,
    SimpleUniqueIdentifier,
)


class PdIdentifier(SimpleUniqueIdentifier):
    random_string_length = 2
    identifier_type = "pd_identifier"
    template = "PD{device_id}{timestamp}{random_string}"
    identifier_cls = SimpleTimestampIdentifier
