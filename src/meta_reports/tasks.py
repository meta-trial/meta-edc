from celery import shared_task


@shared_task
def update_endpoints_table(subject_identifiers: list[str] | None = None):
    from meta_analytics.dataframes import GlucoseEndpointsByDate2  # noqa: PLC0415

    if not subject_identifiers or len(subject_identifiers) > 5:
        cls = GlucoseEndpointsByDate2(verbose=False)
    else:
        cls = GlucoseEndpointsByDate2(subject_identifiers=subject_identifiers, verbose=False)
    return cls.to_model()
