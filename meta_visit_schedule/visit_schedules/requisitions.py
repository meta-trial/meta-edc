from edc_lab_panel.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    fbc_panel,
    hba1c_panel,
    hba1c_poc_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)
from edc_visit_schedule import FormsCollection, Requisition

from meta_labs.lab_profiles import chemistry_panel

requisitions_prn = FormsCollection(
    Requisition(
        show_order=10, panel=blood_glucose_panel, required=True, additional=False
    ),
    Requisition(
        show_order=20, panel=blood_glucose_poc_panel, required=True, additional=False
    ),
    Requisition(show_order=30, panel=hba1c_poc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=hba1c_panel, required=True, additional=False),
    Requisition(show_order=50, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=60, panel=chemistry_panel, required=True, additional=False),
    Requisition(show_order=70, panel=lft_panel, required=True, additional=False),
    Requisition(show_order=80, panel=rft_panel, required=True, additional=False),
    Requisition(show_order=90, panel=lipids_panel, required=True, additional=False),
    name="requisitions_prn",
)

requisitions_d1 = FormsCollection(
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_day1",
)

requisitions_w2 = FormsCollection(name="requisitions_week2")

requisitions_1m = FormsCollection(name="requisitions_month1")

requisitions_3m = FormsCollection(
    Requisition(show_order=10, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_month3",
)

requisitions_6m = FormsCollection(
    Requisition(show_order=10, panel=chemistry_panel, required=True, additional=False),
    Requisition(show_order=20, panel=hba1c_poc_panel, required=True, additional=False),
    name="requisitions_default",
)

requisitions_9m = FormsCollection(
    Requisition(show_order=10, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_month97",
)

requisitions_12m = FormsCollection(
    Requisition(
        show_order=10, panel=blood_glucose_poc_panel, required=True, additional=False
    ),
    Requisition(show_order=20, panel=hba1c_poc_panel, required=True, additional=False),
    Requisition(show_order=30, panel=fbc_panel, required=True, additional=False),
    Requisition(show_order=40, panel=chemistry_panel, required=True, additional=False),
    name="requisitions_month12",
)
