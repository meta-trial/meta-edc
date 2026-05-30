Conversion to new

```bash
uv run --dev manage.py migrate --settings=meta_edc.settings.debug && \
uv run --dev manage.py fix_historical_stock_state && \
uv run --dev manage.py bootstrap_stock_transactions && \
uv run --dev manage.py fix_historical_stock_state && \
uv run --dev manage.py check_stock_ledger
````

Stocks with existing transactions (skipped):

```
    3HMJHK
    3XYGB2
    7YPNBR
    8EV77B
    8RVNHH
    FAGBBK
    FFFJCY
    FG2GVY
    FTYPFY
    HPYXAJ
    KPFTQU
    N3ZQ46
    PNZ444
    QTNKBJ
    QW7E9J
    R4UV68
    TDAQWT
    THDMHK
    ZEG4QR
    ZT6WN9
```

DISCREPANCIES (20):

```
    PNZ444
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    8EV77B
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FFFJCY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    HPYXAJ
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    N3ZQ46
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    THDMHK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    ZEG4QR
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    3HMJHK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FAGBBK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    3XYGB2
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    ZT6WN9
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    KPFTQU
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    8RVNHH
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    FG2GVY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    R4UV68
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    QW7E9J
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FTYPFY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    7YPNBR
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    TDAQWT
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    QTNKBJ
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
```

Today's run

Stocks with existing transactions (skipped):

    3HMJHK
    3XYGB2
    7YPNBR
    8EV77B
    8RVNHH
    FAGBBK
    FFFJCY
    FG2GVY
    FTYPFY
    HPYXAJ
    KPFTQU
    N3ZQ46
    PNZ444
    QTNKBJ
    QW7E9J
    R4UV68
    TDAQWT
    THDMHK
    ZEG4QR
    ZT6WN9

P2

    [in_transit] 0 stocks to fix (will update)
    [allocation] 0 dispensed stocks with non-null allocation (will update)
    [stored_at_location] 0 dispensed stocks with stored_at_location=True (will update)
    [qty_delta] 0 bootstrapped TXN_RECEIVED rows to fix (will update)
    [repack_consumed] 4 RepackRequest rows missing TXN_REPACK_CONSUMED (will create)
    Created 0 rows.
    [repack_consumed_qty] 2 TXN_REPACK_CONSUMED rows with qty_delta=0 but stock.qty_out=1 (
    will update)
    Updated 2 rows.
    [invalid_state] 0 bulk stocks incorrectly marked dispensed (will flag)
    [bulk_location] 0 bulk stocks with non-central location (will update)
    [repack_child_location] 0 repacked child stocks with wrong location (will update)
    [bootstrapped_txn_locations] 24344 bootstrapped transactions with wrong from/to
    location (will update)
    Updated 24344 rows.
    [allocation_backpointer] 0 allocations missing stock back-pointer (will update)

DISCREPANCIES (20):

    PNZ444
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    8EV77B
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FFFJCY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    HPYXAJ
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    N3ZQ46
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    THDMHK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    ZEG4QR
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    3HMJHK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FAGBBK
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    3XYGB2
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    ZT6WN9
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    KPFTQU
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    8RVNHH
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=24556.00
    FG2GVY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    R4UV68
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    QW7E9J
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    FTYPFY
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    7YPNBR
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    TDAQWT
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00
    QTNKBJ
    confirmed: expected=False actual=True
    qty_in: expected=0 actual=1.00
    unit_qty_in: expected=0 actual=16000.00

    Checked 16044 stocks: 16003 OK, 20 with discrepancies, 21 with no transactions.

pre

```python
{
    'stocks_total': 16044,
    'stocks_dispensed': 10215,
    'stocks_in_transit': 12172,
    'stocks_stored': 1764,
    'stocks_confirmed_at_location': 12048,
    'active_allocations': 12174,
    'dispense_items': 10215,
    'transfer_items': 12172
}

```

post

```python
from edc_pharmacy.models import Stock, Allocation, StockTransferItem, DispenseItem

print({
    "stocks_total": Stock.objects.count(),
    "stocks_dispensed": Stock.objects.filter(dispensed=True).count(),
    "stocks_in_transit": Stock.objects.filter(in_transit=True).count(),
    "stocks_stored": Stock.objects.filter(stored_at_location=True).count(),
    "stocks_confirmed_at_location": Stock.objects.filter(confirmed_at_location=True).count(),
    "active_allocations": Allocation.objects.count(),  # OneToOne, pre-refactor
    "dispense_items": DispenseItem.objects.count(),
    "transfer_items": StockTransferItem.objects.count(),
})
```

```python
{
    'stocks_total': 16044,
    'stocks_dispensed': 10215,
    'stocks_in_transit': 120,
    'stocks_stored': 1763,
    'stocks_confirmed_at_location': 12048,
    'active_allocations': 12174,
    'dispense_items': 10215,
    'transfer_items': 12172
}
```

DISCREPANCIES (20):

    PNZ444
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    8EV77B
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    FFFJCY
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=24556.00
    HPYXAJ
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    N3ZQ46
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    THDMHK
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=24556.00
    ZEG4QR
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    3HMJHK
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    FAGBBK
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=24556.00
    3XYGB2
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    ZT6WN9
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    KPFTQU
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    8RVNHH
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=24556.00
    FG2GVY
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    R4UV68
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    QW7E9J
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    FTYPFY
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    7YPNBR
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    TDAQWT
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00
    QTNKBJ
    confirmed: expected=False  actual=True
    qty_in: expected=0  actual=1.00
    unit_qty_in: expected=0  actual=16000.00

Dispensed but still showing as stored at location

    94UQKG Mwananyamala Hospital None None

in_transit=True total: 12172

    ...with ConfirmationAtLocationItem: 12048
    ...dispensed: 10214
    ...genuinely in transit (neither received nor dispensed): 120
