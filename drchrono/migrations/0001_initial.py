# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-05 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.IntegerField()),
                ("doctor_id", models.IntegerField()),
                ("patient_id", models.IntegerField()),
                ("exam_room", models.IntegerField()),
                ("is_walk_in", models.BooleanField(default=False)),
                ("scheduled_time", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            (b"Arrived", b"Arrived"),
                            (b"Checked In", b"Checked In"),
                            (b"In Room", b"In Room"),
                            (b"Cancelled", b"Cancelled"),
                            (b"Complete", b"Complete"),
                            (b"Confirmed", b"Confirmed"),
                            (b"In Session", b"In Session"),
                            (b"No Show", b"No Show"),
                            (b"Not Confirmed", b"Not Confirmed"),
                            (b"Rescheduled", b"Rescheduled"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("reason", models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=500)),
                ("last_name", models.CharField(max_length=500)),
                ("api_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("api_id", models.IntegerField()),
                ("doctor_id", models.IntegerField()),
                ("first_name", models.CharField(max_length=500)),
                ("middle_name", models.CharField(max_length=500, null=True)),
                ("last_name", models.CharField(max_length=500)),
                ("date_of_first_appointment", models.DateField(null=True)),
                ("address", models.CharField(max_length=500)),
                ("city", models.CharField(max_length=500)),
                ("state", models.CharField(max_length=2)),
                ("zip_code", models.CharField(max_length=5)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            (b"Male", b"Male"),
                            (b"Female", b"Female"),
                            (b"Other", b"Other"),
                        ],
                        max_length=10,
                    ),
                ),
                ("ethnicity", models.CharField(max_length=50)),
                (
                    "social_security_number",
                    models.CharField(blank=True, max_length=11, null=True),
                ),
            ],
        ),
    ]
