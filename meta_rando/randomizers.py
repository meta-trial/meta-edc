from edc_constants.constants import FEMALE, MALE
from edc_randomization import Randomizer
from edc_randomization.randomization_list_importer import (
    RandomizationListImporter,
    RandomizationListImportError,
)
from edc_randomization.site_randomizers import site_randomizers

from meta_edc.meta_version import PHASE_THREE


class RandomizationListImporterPhaseThree(RandomizationListImporter):
    """A class to import the Phase Three randomization list CSV"""

    csv_gender_column = "gender"

    def get_extra_import_options(self, row):
        return dict(gender=self.validate_gender(row))

    def validate_gender(self, row):
        if row[self.csv_gender_column] not in [MALE, FEMALE]:
            raise RandomizationListImportError(
                f"Invalid value for gender. Got {row[self.csv_gender_column]}."
            )
        return row[self.csv_gender_column]


class RandomizerPhaseThree(Randomizer):

    name = PHASE_THREE
    model = "meta_rando.randomizationlist"
    filename = "randomization_list_phase_three.csv"
    importer_cls = RandomizationListImporterPhaseThree

    def __init__(self, gender=None, **kwargs):
        self.gender = gender
        super().__init__(**kwargs)

    @property
    def extra_required_instance_attrs(self):
        """Returns a dict of extra attributes that must have
        value on self.
        """
        return dict(gender=self.gender)

    @property
    def extra_model_obj_options(self):
        """Returns a dict of extra key/value pair for filtering the
        "rando" model.
        """
        return dict(gender=self.gender)

    @classmethod
    def get_extra_list_display(cls):
        """Returns a list of tuples of (pos, field name) for ModelAdmin"""
        return [(4, "gender")]


site_randomizers.register(RandomizerPhaseThree)
