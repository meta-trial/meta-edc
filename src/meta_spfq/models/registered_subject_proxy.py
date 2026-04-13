from edc_registration.models import RegisteredSubject


class RegisteredSubjectProxy(RegisteredSubject):
    def __str__(self):
        return self.subject_identifier

    class Meta:
        proxy = True
