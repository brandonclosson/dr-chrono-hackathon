from datetime import datetime

from django.db import models


class AppointmentTodayManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return (
            super(AppointmentTodayManager, self)
            .get_queryset()
            .filter(
                scheduled_time__year=date.year,
                scheduled_time__month=date.month,
                scheduled_time__day=date.day,
            )
        )


class AppointmentUpcomingManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return (
            super(AppointmentUpcomingManager, self)
            .get_queryset()
            .filter(
                scheduled_time__year=date.year,
                scheduled_time__month=date.month,
                scheduled_time__day=date.day,
                status__in=("Checked In", "Arrived", ""),
            )
        )


class AppointmentCurrentManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return (
            super(AppointmentCurrentManager, self)
            .get_queryset()
            .filter(
                scheduled_time__year=date.year,
                scheduled_time__month=date.month,
                scheduled_time__day=date.day,
                status="In Room",
            )
        )


class AppointmentCompleteManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return (
            super(AppointmentCompleteManager, self)
            .get_queryset()
            .filter(
                scheduled_time__year=date.year,
                scheduled_time__month=date.month,
                scheduled_time__day=date.day,
                status="Complete",
            )
        )


class AppointmentOtherManager(models.Manager):
    def get_queryset(self):
        date = datetime.now()
        return (
            super(AppointmentOtherManager, self)
            .get_queryset()
            .filter(
                scheduled_time__year=date.year,
                scheduled_time__month=date.month,
                scheduled_time__day=date.day
            ).exclude(
                status__in=("Complete", "", "In Room", "Arrive", "Checked In", "In Session"),
            )
        )
