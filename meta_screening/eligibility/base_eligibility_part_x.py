import abc

from .eligibility import Eligibility


class RequiredFieldValueMissing(Exception):
    pass


class BaseEligibilityPartX(Eligibility):
    @abc.abstractmethod
    def assess_eligibility(self):
        pass

    @classmethod
    def get_required_fields(cls):
        return []

    @abc.abstractmethod
    def get_reasons_ineligible(self, *args):
        return None

    def check_for_required_field_values(self, exception_cls=None):
        required_values = [getattr(self.obj, f) for f in self.get_required_fields()]
        if not all(required_values):
            missing_values = {
                f: getattr(self.obj, f)
                for f in self.get_required_fields()
                if not getattr(self.obj, f)
            }
            raise RequiredFieldValueMissing(
                f"Missing required values. Got {missing_values}"
            )
