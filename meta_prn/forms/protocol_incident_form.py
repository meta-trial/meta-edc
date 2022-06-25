from edc_protocol_violation.forms import ProtocolIncidentForm as Base

from ..models import ProtocolDeviationViolation


class ProtocolIncidentForm(Base):
    class Meta:
        model = ProtocolDeviationViolation
        fields = "__all__"
