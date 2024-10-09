from edc_pharmacy.models import Rx as BaseRx


class Rx(BaseRx):
    """A proxy model of edc_pharmacy.Rx.

    A model for the prescription.

    For autocomplete only.
    """

    def save(self, *args, **kwargs):
        raise NotImplementedError(
            "This proxy model may not be saved. Permissions should be view only"
        )

    class Meta:
        proxy = True
