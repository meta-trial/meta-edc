from edc_randomization import Randomizer
from edc_randomization.site_randomizers import site_randomizers

from meta_edc.meta_version import PHASE_THREE, PHASE_TWO, get_meta_version


class RandomizerPhaseTwo(Randomizer):

    name = PHASE_TWO


class RandomizerPhaseThree(Randomizer):

    name = PHASE_THREE
    model = "meta_rando.randomizationlist"

    def __init__(self, gender=None, **kwargs):
        self.gender = gender
        super().__init__(**kwargs)

    @property
    def extra_required_attrs(self):
        return dict(gender=self.gender)


if get_meta_version() == PHASE_TWO:
    site_randomizers.register(RandomizerPhaseTwo)

if get_meta_version() == PHASE_THREE:
    site_randomizers.register(RandomizerPhaseThree)
