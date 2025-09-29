from celery import shared_task


@shared_task
def update_endpoints_table(subject_identifiers: list[str] | None = None):
    from meta_analytics.dataframes import GlucoseEndpointsByDate  # noqa: PLC0415

    if len(subject_identifiers) > 5:
        cls = GlucoseEndpointsByDate()
    else:
        cls = GlucoseEndpointsByDate(subject_identifiers=subject_identifiers)
    cls.run()
    return cls.to_model()
