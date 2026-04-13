from .subject_consent_spfq import SubjectConsentSpfq


class SubjectConsentSpfqForWithdrawal(SubjectConsentSpfq):
    """A model completed by the user that captures the ICF for SPFQ
    for Withdrawal.
    """

    class Meta:
        proxy = True
        verbose_name = "Subject Consent SPFQ for Withdrawal"
        verbose_name_plural = "Subject Consent SPFQ for Withdrawal"
