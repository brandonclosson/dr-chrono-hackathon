from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, View

from drchrono.endpoints import AppointmentEndpoint
from drchrono.models import Appointment, Doctor
from drchrono.utils import get_average_wait_time


class AppointmentListView(LoginRequiredMixin, TemplateView):

    template_name = "appointment_list.html"

    def get_context_data(self, **kwargs):
        kwargs = super(AppointmentListView, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor = Doctor.objects.first()
        appointments = Appointment.today.all()
        upcoming_appointments = Appointment.upcoming.all()
        kwargs["doctor"] = doctor
        kwargs["upcoming_appointments"] = upcoming_appointments
        kwargs["now"] = datetime.now()
        return kwargs


class UpcomingAppointmentListView(View):
    def get(self, request):
        appointments = Appointment.upcoming.all()
        context = {"appointments": appointments}
        return render(request, "appointment_upcoming_list.html", context)


class CompletedAppointmentListView(View):
    def get(self, request):
        appointments = Appointment.complete.all()
        context = {"appointments": appointments}
        return render(request, "appointment_complete_list.html", context)


class CurrentAppointmentListView(View):
    def get(self, request):
        appointments = Appointment.current.all()
        context = {"appointments": appointments}
        return render(request, "appointment_current_list.html", context)


class AverageWaitTimeView(View):
    def get(self, request):
        average_wait_time = get_average_wait_time()
        context = {"average_wait_time": average_wait_time}
        return render(request, "average_wait_time.html", context)


class UpdateAppointmentView(View):
    def post(self, request):
        status = self.request.POST.get("status")
        appointment_id = self.request.POST.get("id")
        appointment = Appointment.objects.get(pk=appointment_id)
        if status == "In Room":
            appointment.final_wait_time = appointment.wait_time
        appointment.status = status
        appointment.save()
        appointment_api = AppointmentEndpoint(self.request.session["access_token"])
        appointment_api.update(appointment.api_id, {"status": status})

        return JsonResponse({"status": "success"})
