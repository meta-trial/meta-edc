from celery import shared_task


@shared_task
def update_unmanaged_table(subject_identifiers: list[str] | None = None):
    from meta_analytics.dataframes import GlucoseEndpointsByDate

    cls = GlucoseEndpointsByDate(subject_identifiers=subject_identifiers)
    cls.run()
    return cls.to_model(subject_identifiers=subject_identifiers)
