from edc_lab_panel.panels import (
    blood_glucose_panel,
    fbc_panel,
    hba1c_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_visit_schedule import FormsCollection, Requisition

requisitions_prn = FormsCollection(
    Requisition(show_order=200, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=220, panel=hba1c_panel, required=True, additional=False),
    Requisition(show_order=230, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=240, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=260, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=270, panel=insulin_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = FormsCollection(
    Requisition(show_order=200, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_unscheduled",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=insulin_panel, required=True, additional=False),
    name="requisitions_day1",
)

requisitions_w2 = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_week2",
)

requisitions_1m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month1",
)

requisitions_3m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    name="requisitions_month3",
)

requisitions_6m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    name="requisitions_month6",
)

requisitions_9m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month9",
)

requisitions_12m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month12",
)

requisitions_15m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month15",
)

requisitions_18m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=20, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month18",
)

requisitions_21m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month21",
)

requisitions_24m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month24",
)

requisitions_27m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month27",
)

requisitions_30m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month30",
)

requisitions_33m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    name="requisitions_month33",
)

requisitions_36m = FormsCollection(
    Requisition(show_order=10, panel=blood_glucose_panel, required=True, additional=False),
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month36",
)
