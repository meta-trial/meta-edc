#!/usr/bin/env python
import sys
from pathlib import Path

from edc_test_settings.default_test_settings import DefaultTestSettings

from .get_test_setting_opts import get_test_setting_opts

app_name = "meta_edc"
base_dir = Path(__file__).parent.parent
project_settings = DefaultTestSettings(**get_test_setting_opts(app_name, base_dir)).settings

for k, v in project_settings.items():
    setattr(sys.modules[__name__], k, v)
