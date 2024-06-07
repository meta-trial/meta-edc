from edc_lab_panel.panels import (
    fbc_panel,
    hba1c_panel,
    insulin_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_visit_schedule.visit import Requisition, RequisitionCollection

requisitions_prn = RequisitionCollection(
    Requisition(show_order=220, panel=hba1c_panel, required=True, additional=False),
    Requisition(show_order=230, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=240, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=250, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=260, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=270, panel=insulin_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_unscheduled = RequisitionCollection(name="requisitions_unscheduled")

requisitions_d1 = RequisitionCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=60, panel=insulin_panel, required=True, additional=False),
    name="requisitions_day1",
)

requisitions_w2 = RequisitionCollection(name="requisitions_week2")

requisitions_1m = RequisitionCollection(name="requisitions_month1")

requisitions_3m = RequisitionCollection(
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    name="requisitions_month3",
)

requisitions_6m = RequisitionCollection(
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    name="requisitions_month6",
)

requisitions_9m = RequisitionCollection(name="requisitions_month9")

requisitions_12m = RequisitionCollection(
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month12",
)

requisitions_15m = RequisitionCollection(name="requisitions_month15")

requisitions_18m = RequisitionCollection(
    Requisition(show_order=20, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month18",
)

requisitions_21m = RequisitionCollection(name="requisitions_month21")

requisitions_24m = RequisitionCollection(
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month24",
)

requisitions_27m = RequisitionCollection(name="requisitions_month27")

requisitions_30m = RequisitionCollection(
    Requisition(show_order=20, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=30, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month30",
)

requisitions_33m = RequisitionCollection(name="requisitions_month33")

requisitions_36m = RequisitionCollection(
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month36",
)

requisitions_39m = RequisitionCollection(name="requisitions_month39")
requisitions_42m = RequisitionCollection(name="requisitions_month42")
requisitions_45m = RequisitionCollection(name="requisitions_month45")

requisitions_48m = RequisitionCollection(
    Requisition(show_order=30, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=40, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=50, panel=lipids_panel, required=True, additional=False),
    Requisition(show_order=60, panel=fbc_panel, required=True, additional=False),
    name="requisitions_month48",
)
