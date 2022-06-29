from django.db import models
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager

from .ae_initial import AeInitial


class BaseManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, action_identifier, ae_initial_action_identifier):
        ae_initial = AeInitial.objects.get(action_identifier=ae_initial_action_identifier)
        return self.get(action_identifier=action_identifier, ae_initial=ae_initial)


class AeManager(BaseManager):

    use_in_migrations = True


class CurrentSiteManager(BaseManager, BaseCurrentSiteManager):

    use_in_migrations = True
