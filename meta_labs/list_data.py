from edc_list_data import PreloadData


model_data = {
    "edc_lab.consignee": [
        {
            "name": "The META Trial",
            "contact_name": "Sokoine Kivuyo",
            "address": "NIMR Tanzania",
            "postal_code": "-",
            "city": "Dar es Salaam",
            "state": None,
            "country": "Tanzania",
            "telephone": "+255763244779",
            "mobile": "+255763244779",
            "fax": None,
            "email": "sokoinele@yahoo.co.uk",
        }
    ]
}

unique_field_data = {"edc_lab.consignee": {"name": ("-", "-")}}

preload_data = PreloadData(
    list_data=None, model_data=model_data, unique_field_data=unique_field_data
)
