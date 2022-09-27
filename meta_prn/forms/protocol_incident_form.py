from edc_protocol_incident.forms import ProtocolIncidentForm as Base

from ..models import ProtocolIncident


class ProtocolIncidentForm(Base):
    class Meta(Base.Meta):
        model = ProtocolIncident
        fields = "__all__"
