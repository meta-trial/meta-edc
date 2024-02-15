from edc_visit_schedule.visit import Crf, CrfCollection

crfs_pregnancy = CrfCollection(
    Crf(show_order=100, model="meta_subject.delivery"),
    name="pregnancy",
)
