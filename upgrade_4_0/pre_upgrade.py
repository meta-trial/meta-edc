# scripts/pre_upgrade_invariants.py
# Run via: manage.py shell --settings=<your.settings> < scripts/pre_upgrade_invariants.py
import json
from decimal import Decimal
from pathlib import Path

from django.db.models import Sum
from edc_pharmacy.models import (
    Allocation,
    ConfirmationAtLocationItem,
    DispenseItem,
    Stock,
    StockTransferItem,
    StorageBinItem,
)


def _as_int(x):
    return int(x or 0)


def _as_str_dec(x):
    return str(x or Decimal(0))


snapshot = {
    # Totals — must NOT change across upgrade.
    "stocks_total": Stock.objects.count(),
    "dispense_items": DispenseItem.objects.count(),
    "stock_transfer_items": StockTransferItem.objects.count(),
    "storage_bin_items": StorageBinItem.objects.count(),
    "confirmation_at_location_items": ConfirmationAtLocationItem.objects.count(),
    # Stock cache columns — must NOT change across upgrade (the whole point
    # of `fix_historical_stock_state` is that the corrections are idempotent
    # *given the current data*).
    "stocks_confirmed": Stock.objects.filter(confirmed=True).count(),
    "stocks_confirmed_at_location": Stock.objects.filter(confirmed_at_location=True).count(),
    "stocks_in_transit": Stock.objects.filter(in_transit=True).count(),
    "stocks_stored_at_location": Stock.objects.filter(stored_at_location=True).count(),
    "stocks_dispensed": Stock.objects.filter(dispensed=True).count(),
    "stocks_allocated": Stock.objects.filter(allocation__isnull=False).count(),
    # Aggregate qty — must NOT change.
    "qty_in_total": _as_str_dec(Stock.objects.aggregate(s=Sum("qty_in"))["s"]),
    "qty_out_total": _as_str_dec(Stock.objects.aggregate(s=Sum("qty_out"))["s"]),
    "unit_qty_in_total": _as_str_dec(Stock.objects.aggregate(s=Sum("unit_qty_in"))["s"]),
    "unit_qty_out_total": _as_str_dec(Stock.objects.aggregate(s=Sum("unit_qty_out"))["s"]),
    # Allocation counts. Note: in 3.1.5 Allocation was a OneToOneField and
    # the row was deleted when stock was dispensed. In 4.0.0 it's a sticky
    # ForeignKey and rows may accumulate (ended_datetime IS NOT NULL). The
    # pre-snapshot number is therefore a LOWER bound on the post-snapshot.
    "allocations": Allocation.objects.count(),
    # Subjects with at least one allocated stock — should not change.
    "subjects_with_allocations": (
        Allocation.objects.values("subject_identifier").distinct().count()
    ),
    # Allocation back-pointer health — pre-upgrade many will be NULL; that's
    # the legacy bug. Post-upgrade should be zero.
    "allocations_with_null_stock": Allocation.objects.filter(stock__isnull=True).count(),
}

with Path("upgrade_invariants_pre.json").open("w") as f:
    json.dump(snapshot, f, indent=2, sort_keys=True)
print(json.dumps(snapshot, indent=2, sort_keys=True))  # noqa T201
