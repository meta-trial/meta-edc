from edc_visit_schedule import Crf, FormsCollection

crfs_pregnancy = FormsCollection(
    Crf(show_order=100, model="meta_subject.delivery"),
    name="pregnancy",
)
