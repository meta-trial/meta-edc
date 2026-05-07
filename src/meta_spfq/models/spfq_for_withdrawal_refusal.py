from .spfq_refusal import SpfqRefusal


class SpfqForWithdrawalRefusal(SpfqRefusal):
    class Meta:
        proxy = True
        verbose_name = "SPFQ: Refusal for WITHDRAWAL interview"
        verbose_name_plural = "SPFQ: Refusal for WITHDRAWAL interview"
