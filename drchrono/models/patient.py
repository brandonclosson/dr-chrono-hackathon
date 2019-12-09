from django.db import models


PATIENT_GENDER_CHOICES = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))


class Patient(models.Model):
    api_id = models.IntegerField()
    doctor_id = models.IntegerField()
    first_name = models.CharField(max_length=500)
    middle_name = models.CharField(max_length=500, null=True)
    last_name = models.CharField(max_length=500)
    date_of_first_appointment = models.DateField(null=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    gender = models.CharField(max_length=10, choices=PATIENT_GENDER_CHOICES)
    ethnicity = models.CharField(max_length=50)
    social_security_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True)
