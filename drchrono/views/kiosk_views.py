from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import FormView, TemplateView, UpdateView
from social_django.models import UserSocialAuth

from drchrono.endpoints import APIException, AppointmentEndpoint, PatientEndpoint
from drchrono.forms import PatientSignInForm, PatientDemographicsForm
from drchrono.models import Appointment, Patient


class PatientCheckInView(LoginRequiredMixin, FormView):
    """
    Patient Sign In screen on kiosk.
    """

    template_name = "patient_checkin.html"
    form_class = PatientSignInForm
    success_url = "/demographics/"

    def dispatch(self, request, *args, **kwargs):
        request.session["patient_id"] = None
        request.session["appointment_ids"] = None
        return super(PatientCheckInView, self).dispatch(request, args, kwargs)

    def form_valid(self, form):
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]

        try:
            patient = Patient.objects.get(first_name=first_name, last_name=last_name)
        except ObjectDoesNotExist:
            return render(
                self.request,
                "patient_checkin.html",
                {"error": "Patient not found", "form": form},
            )

        appointments = Appointment.today.filter(
            patient_id=patient.api_id, status__in=("", "Arrived")
        )
        if not appointments:
            return render(
                self.request,
                "patient_checkin.html",
                {"error": "No appointment found for today", "form": form},
            )

        self.request.session["patient_id"] = patient.api_id
        self.request.session["appointment_ids"] = [
            appointment.api_id for appointment in appointments
        ]
        return super(PatientCheckInView, self).form_valid(form)


class PatientDemographicsView(LoginRequiredMixin, UpdateView):
    """
    Patient demographics update screen on kiosk
    """

    model_class = Patient
    success_url = "/check-in-success/"
    template_name = "patient_demographics.html"
    form_class = PatientDemographicsForm

    def form_valid(self, form):
        patients_api = PatientEndpoint(self.request.session["access_token"])
        try:
            patients_api.update(self.request.session["patient_id"], form.cleaned_data)
        except APIException:
            return render(
                self.request,
                "patient_checkin.html",
                {"error": "There was an error updating your information", "form": form},
            )
        appointments_api = AppointmentEndpoint(self.request.session["access_token"])
        for appointment_id in self.request.session["appointment_ids"]:
            try:
                appointments_api.update(appointment_id, {"status": "Arrived"})
            except APIException:
                return render(
                    self.request,
                    "patient_checkin.html",
                    {
                        "error": "There was an error checking in to your appointment",
                        "form": form,
                    },
                )
            appointment = Appointment.objects.get(api_id=appointment_id)
            appointment.status = "Arrived"
            appointment.check_in_time = timezone.now()
            appointment.save()
        return super(PatientDemographicsView, self).form_valid(form)

    def get_object(self):
        patient = Patient.objects.get(api_id=self.request.session["patient_id"])
        return patient

    def get_context_data(self, **kwargs):
        kwargs = super(PatientDemographicsView, self).get_context_data(**kwargs)
        kwargs["appointments"] = Appointment.objects.filter(
            api_id__in=self.request.session["appointment_ids"]
        )
        return kwargs


class PatientCheckInSuccessView(LoginRequiredMixin, TemplateView):
    """
    Patient Check In Success message on kiosk
    """

    template_name = "patient_checkin_success.html"

    def get_context_data(self, **kwargs):
        kwargs = super(PatientCheckInSuccessView, self).get_context_data(**kwargs)
        kwargs["appointments"] = Appointment.objects.filter(
            api_id__in=self.request.session["appointment_ids"]
        )
        return kwargs
