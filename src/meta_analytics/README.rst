pip install -U pdfkit great_tables scipy django_pandas dj_notebook

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from django_pandas.io import read_frame
from dj_notebook import activate

from meta_screening.models import SubjectScreening

plus = activate(dotenv_file="/Users/erikvw/source/edc_source/meta-edc/.env")

qs = SubjectScreening.objects.all()

df = read_frame(qs)
