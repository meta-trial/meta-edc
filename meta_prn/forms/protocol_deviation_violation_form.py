from edc_protocol_violation.forms import ProtocolDeviationViolationForm as Base

from ..models import ProtocolDeviationViolation


class ProtocolDeviationViolationForm(Base):
    class Meta:
        model = ProtocolDeviationViolation
        fields = "__all__"
