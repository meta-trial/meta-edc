from clinicedc_tests.config import func_main

if __name__ == "__main__":
    func_main(
        "tests.test_settings",
        "tests",
        "meta_pharmacy",
        "meta_ae.tests",
        "meta_consent.tests",
        "meta_dashboard.tests",
        "meta_edc.tests",
        "meta_labs.tests",
        "meta_lists.tests",
        "meta_prn.tests",
        "meta_rando.tests",
        "meta_screening.tests",
        "meta_subject.tests",
        "meta_visit_schedule.tests",
    )
