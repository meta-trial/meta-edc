from .subject_consent_spfq import SubjectConsentSpfq


class SubjectConsentSpfqForWithdrawal(SubjectConsentSpfq):
    """A model completed by the user that captures the ICF for SPFQ
    for Withdrawal.
    """

    class Meta:
        proxy = True
        verbose_name = "SPFQ: Consent for WITHDRAWAL interview"
        verbose_name_plural = "SPFQ: Consent for WITHDRAWAL interview"
