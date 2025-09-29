from edc_lab import ProcessingProfile, disposable, wb

fbc_processing = ProcessingProfile(name="FBC", aliquot_type=wb)

chemistry_processing = ProcessingProfile(name="Chem", aliquot_type=wb)

chemistry_alt_processing = ProcessingProfile(name="Chem + ALT", aliquot_type=wb)

hba1c_processing = ProcessingProfile(name="HbA1c", aliquot_type=wb)

blood_glucose_processing = ProcessingProfile(name="Blood Glucose", aliquot_type=wb)

poc_processing = ProcessingProfile(name="POC", aliquot_type=disposable)
