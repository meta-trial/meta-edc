from datetime import datetime
from zoneinfo import ZoneInfo

from clinicedc_constants import FEMALE, MALE
from edc_consent.consent_definition import ConsentDefinition
from edc_consent.consent_definition_extension import ConsentDefinitionExtension
from edc_consent.site_consents import site_consents
from edc_protocol.research_protocol_config import ResearchProtocolConfig

consent_v1 = ConsentDefinition(
    "meta_consent.subjectconsentv1",
    version="1",
    start=ResearchProtocolConfig().study_open_datetime,
    end=ResearchProtocolConfig().study_close_datetime,
    age_min=18,
    age_is_adult=18,
    age_max=110,
    gender=[MALE, FEMALE],
    screening_model=[
        "meta_screening.subjectscreening",
        "meta_screening.screeningpartone",
        "meta_screening.screeningparttwo",
        "meta_screening.screeningpartthree",
    ],
    timepoints=list(range(1, 14 + 1)),
)

consent_v1_ext = ConsentDefinitionExtension(
    "meta_consent.subjectconsentv1ext",
    version="1.1",
    start=datetime(2024, 12, 16, tzinfo=ZoneInfo("UTC")),
    extends=consent_v1,
    timepoints=[15, 16, 17, 18],
)

site_consents.register(consent_v1, extended_by=consent_v1_ext)
