from .clinic_codenames import clinic_codenames

auditor_codenames = [c for c in clinic_codenames if "view_" in c]

auditor_codenames.sort()
