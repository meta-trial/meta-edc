#!/usr/bin/env python
import sys
from pathlib import Path

from clinicedc_tests.config import DefaultTestSettings

from .get_test_setting_opts import get_test_setting_opts

app_name = "meta_edc"
base_dir = Path(__file__).parent.parent
project_settings = DefaultTestSettings(
    **get_test_setting_opts(app_name, base_dir),
    MULTISITE_TIME_ZONES={  # one country so technically not necessary
        10: "Africa/Dar_es_Salaam",
        20: "Africa/Dar_es_Salaam",
        30: "Africa/Dar_es_Salaam",
        40: "Africa/Dar_es_Salaam",
        50: "Africa/Dar_es_Salaam",
        60: "Africa/Dar_es_Salaam",
    },
).settings

for k, v in project_settings.items():
    setattr(sys.modules[__name__], k, v)

sys.stdout.write(f"Reading settings from: {__file__}\n")
