import csv
import sys
from pathlib import Path

from clinicedc_constants import FEMALE, MALE
from django.apps import apps as django_apps
from django.conf import settings
from tqdm import tqdm

from .constants import GTE_35__LTE_49, GTE_50, LT_35


def import_spfq_list():
    spfq_list_model_cls = django_apps.get_model("meta_spfq.spfqlist")
    if spfq_list_model_cls.objects.all().count() == 0:
        path = Path(settings.ETC_DIR) / getattr(
            settings, "META_SPFQ_LIST_FILENAME", "spfq_list.csv"
        )
        if path.exists():
            with path.open("r") as f:
                reader = csv.DictReader(f)
                all_rows = [{k: v.strip() for k, v in row.items() if k} for row in reader]
                for row in all_rows:
                    if row["gender"] == "male":
                        row["gender"] = MALE
                    elif row["gender"] == "female":
                        row["gender"] = FEMALE
                    if row["weight_bin"] == "<35":
                        row["weight_bin"] = LT_35
                    elif row["weight_bin"] == "35-49":
                        row["weight_bin"] = GTE_35__LTE_49
                    elif row["weight_bin"] == ">=50":
                        row["weight_bin"] = GTE_50
                for row in tqdm(all_rows, total=len(all_rows)):
                    spfq_list_model_cls.objects.create(filename=str(path.name), **row)
            sys.stdout.write(
                f"\nImported {spfq_list_model_cls.objects.all().count()} "
                "records into model SPFQ.\n"
            )
