drop table edc_pharmacy_dispenseditem;
drop table edc_pharmacy_prescriptionitem;
drop table edc_pharmacy_prescription;
drop table edc_pharmacy_appointment;
drop table edc_pharmacy_dosageguideline;
drop table edc_pharmacy_medication;
delete from django_migrations where app='edc_pharmacy';
