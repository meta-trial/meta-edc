from pathlib import Path

from django.conf import settings


def read_unmanaged_model_sql(filename) -> str:
    file = Path(settings.BASE_DIR) / "meta_reports" / "models" / "unmanaged" / filename
    with file.open("r") as f:
        sql = f.read()
    return sql.replace("\n", " ")
