from django.db import models
from django.utils import timezone

from drchrono.managers import (
    AppointmentCompleteManager,
    AppointmentCurrentManager,
    AppointmentOtherManager,
    AppointmentTodayManager,
    AppointmentUpcomingManager,
)
from patient import Patient

APPOINTMENT_STATUS_CHOICES = (
    ("Arrived", "Arrived"),
    ("Checked In", "Checked In"),
    ("In Room", "In Room"),
    ("Cancelled", "Cancelled"),
    ("Complete", "Complete"),
    ("Confirmed", "Confirmed"),
    ("In Session", "In Session"),
    ("No Show", "No Show"),
    ("Not Confirmed", "Not Confirmed"),
    ("Rescheduled", "Rescheduled"),
)


class Appointment(models.Model):
    api_id = models.IntegerField()
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    exam_room = models.IntegerField()
    is_walk_in = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField()
    status = models.CharField(
        max_length=50, choices=APPOINTMENT_STATUS_CHOICES, blank=True, null=True
    )
    reason = models.CharField(max_length=500)
    check_in_time = models.DateTimeField(null=True)
    final_wait_time = models.IntegerField(null=True)

    complete = AppointmentCompleteManager()
    current = AppointmentCurrentManager()
    other = AppointmentOtherManager()
    today = AppointmentTodayManager()
    upcoming = AppointmentUpcomingManager()
    objects = models.Manager()

    @property
    def patient(self):
        patient = Patient.objects.get(api_id=self.patient_id)
        return patient

    @property
    def wait_time(self):
        if self.final_wait_time:
            return self.final_wait_time
        elif self.status == "Checked In":
            td = timezone.now() - self.check_in_time
            return td.seconds / 60
        return None
