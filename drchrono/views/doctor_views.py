from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint
from drchrono.models import Doctor, Patient


class DoctorWelcome(LoginRequiredMixin, TemplateView):
    """
    The doctor can see what appointments they have today.
    """

    template_name = "doctor_welcome.html"

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider="drchrono")
        access_token = oauth_provider.extra_data["access_token"]
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get 
        doctor details. If this succeeds, we've proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        self.request.session["access_token"] = access_token
        return api.save_doctor()

    def get_today_appointments(self, doctor_id):
        access = self.get_token()
        appointments_api = AppointmentEndpoint(access)
        today = datetime.today()
        appointments = appointments_api.save_appointments(doctor_id, today)
        return appointments

    def get_doctor_patients(self, doctor_id):
        access = self.get_token()
        patients_api = PatientEndpoint(access)
        patients = patients_api.save_patients(doctor_id)
        return patients

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        doctor = self.make_api_request()
        appointment_details = self.get_today_appointments(doctor.api_id)
        patient_details = self.get_doctor_patients(doctor.api_id)
        kwargs["doctor"] = doctor
        kwargs["appointments"] = appointment_details
        kwargs["patients"] = patient_details
        return kwargs
