from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

import views


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^appointments/", views.AppointmentListView.as_view(), name="appointments"),
    url(
        r"^average-wait-time/",
        views.AverageWaitTimeView.as_view(),
        name="average_wait_time",
    ),
    url(
        r"^appointments-by-type/",
        views.AppointmentListAjaxView.as_view(),
        name="appointments_by_type",
    ),
    url(
        r"^update-appointment/",
        views.UpdateAppointmentView.as_view(),
        name="update_appointment",
    ),
    url(
        r"^check-in-success/",
        views.PatientCheckInSuccessView.as_view(),
        name="patient_checkin_success",
    ),
    url(
        r"^demographics/$",
        views.PatientDemographicsView.as_view(),
        name="patient_demographics",
    ),
    url(r"^kiosk/$", views.PatientCheckInView.as_view(), name="kiosk"),
    url(r"^setup/$", views.SetupView.as_view(), name="setup"),
    url(r"^patients/$", views.PatientListView.as_view(), name="patients"),
    url(
        r"^patients/(?P<pk>\d+)/$",
        views.PatientDetailView.as_view(),
        name="patient_detail",
    ),
    url(r"^welcome/$", views.DoctorWelcome.as_view(), name="welcome"),
    url(r"^webhooks/$", views.webhook_view, name="webhooks"),
    url(r"", include("social.apps.django_app.urls", namespace="social")),
]
