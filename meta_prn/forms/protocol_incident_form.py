from edc_protocol_violation.forms import ProtocolIncidentForm as Base

from ..models import ProtocolIncident


class ProtocolIncidentForm(Base):
    class Meta(Base.Meta):
        model = ProtocolIncident
        fields = "__all__"
