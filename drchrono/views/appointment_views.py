from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, View

from drchrono.endpoints import AppointmentEndpoint, APIException
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


class AppointmentListAjaxView(View):
    def get(self, request):
        if self.request.is_ajax():
            appointment_type = self.request.GET.get("appointment_type")
            if appointment_type == "upcoming":
                appointments = Appointment.upcoming.all()
                template = "appointment_upcoming_list.html"
            elif appointment_type == "completed":
                appointments = Appointment.complete.all()
                template = "appointment_complete_list.html"
            elif appointment_type == "current":
                appointments = Appointment.current.all()
                template = "appointment_current_list.html"
            elif appointment_type == "other":
                appointments = Appointment.other.all()
                template = "appointment_other_list.html"
            context = {"appointments": appointments}
            return render(request, template, context)


class AverageWaitTimeView(View):
    def get(self, request):
        average_wait_time = get_average_wait_time()
        context = {"average_wait_time": average_wait_time}
        return render(request, "average_wait_time.html", context)


class UpdateAppointmentView(View):
    def post(self, request):
        if self.request.is_ajax():
            status = self.request.POST.get("status")
            appointment_id = self.request.POST.get("id")
            notes = self.request.POST.get("notes", "")
            try:
                appointment_api = AppointmentEndpoint(
                    self.request.session["access_token"]
                )
                appointment_api.update(appointment_id, {"status": status, "notes": notes})
            except APIException:
                return JsonResponse({"status": "API failure"}, status=500)
            appointment = Appointment.objects.get(api_id=appointment_id)
            if status == "In Room":
                appointment.final_wait_time = appointment.wait_time
            appointment.status = status
            appointment.notes = notes
            appointment.save()

            return JsonResponse({"status": "success"})
