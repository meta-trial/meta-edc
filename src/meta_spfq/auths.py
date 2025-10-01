from edc_auth.get_app_codenames import get_app_codenames
from edc_auth.site_auths import site_auths

META_SPFQ = "meta_spfq"
META_SPFQ_ROLE = "meta_spfq_role"

spfq_codenames = [
    c
    for c in get_app_codenames("meta_spfq")
    if c
    not in ["meta_spfq.add_spfqlist", "meta_spfq.change_spfqlist", "meta_spfq.delete_spfqlist"]
]
site_auths.add_group(*spfq_codenames, name=META_SPFQ)
site_auths.add_role(META_SPFQ, name=META_SPFQ_ROLE)
