from django.core.exceptions import ObjectDoesNotExist
from tqdm import tqdm

from meta_consent.models import SubjectConsent
from meta_rando.models import RandomizationList

from ..models import Label, LotNumber, Rx


class InvalidLotNumber(Exception):
    pass


def get_label_data(lot_no, max_labels: int | None = None) -> list[Label]:
    try:
        lot_no = LotNumber.objects.get(lot_no=lot_no)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("The lot number given is invalid")
    else:
        labels = []
        qs = SubjectConsent.objects.values("subject_identifier", "site_id", "gender").all()
        for obj in tqdm(qs, total=qs.count()):
            if max_labels and len(labels) >= max_labels:
                break
            rando = RandomizationList.objects.get(subject_identifier=obj["subject_identifier"])
            if rando.assignment != lot_no.allocation:
                continue
            rx = Rx.objects.get(subject_identifier=obj["subject_identifier"])
            labels.append(Label.objects.create(rx=rx, lot_no=lot_no))
    return labels
