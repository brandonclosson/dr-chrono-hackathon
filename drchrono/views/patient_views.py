from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView

from drchrono.endpoints import AllergyEndpoint, MedicationEndpoint
from drchrono.models import Doctor, Patient


class PatientListView(LoginRequiredMixin, TemplateView):

    template_name = "patient_list.html"

    def get_context_data(self, **kwargs):
        kwargs = super(PatientListView, self).get_context_data(**kwargs)
        doctor = Doctor.objects.first()
        patients = Patient.objects.filter(doctor_id=doctor.api_id).order_by("last_name")
        kwargs["doctor"] = doctor
        kwargs["patients"] = patients
        return kwargs


class PatientDetailView(LoginRequiredMixin, DetailView):

    model = Patient
    template_name = "patient.html"

    def get_context_data(self, **kwargs):
        kwargs = super(PatientDetailView, self).get_context_data(**kwargs)
        allergies_api = AllergyEndpoint(self.request.session["access_token"])
        allergies = allergies_api.list(params={"patient": kwargs["patient"].api_id})
        medications_api = MedicationEndpoint(self.request.session["access_token"])
        medications = medications_api.list(params={"patient": kwargs["patient"].api_id})
        kwargs["allergies"] = allergies
        kwargs["medications"] = medications
        return kwargs
