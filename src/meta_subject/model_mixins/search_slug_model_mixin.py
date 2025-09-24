from edc_search.model_mixins import SearchSlugModelMixin as Base


class SearchSlugModelMixin(Base):
    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        return *fields, "subject_identifier"

    class Meta:
        abstract = True
