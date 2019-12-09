import hashlib, hmac
import json
import os

from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from drchrono.models import Appointment, Patient

WEBHOOK_SECRET_TOKEN = os.environ["WEBHOOK_SECRET_TOKEN"]


@csrf_exempt
def webhook_view(request):
    if request.method == "GET":
        secret_token = hmac.new(
            WEBHOOK_SECRET_TOKEN, request.GET["msg"], hashlib.sha256
        ).hexdigest()
        return JsonResponse({"secret_token": secret_token})
    else:
        event_type = request.META["HTTP_X_DRCHRONO_EVENT"]
        if event_type == "APPOINTMENT_CREATE":
            new_appointment = json.loads(request.body)["object"]
            Appointment.objects.create(
                api_id=new_appointment["id"],
                doctor_id=new_appointment["doctor"],
                patient_id=new_appointment["patient"],
                exam_room=new_appointment["exam_room"],
                is_walk_in=new_appointment["is_walk_in"],
                scheduled_time=new_appointment["scheduled_time"],
                status=new_appointment["status"],
                reason=new_appointment["reason"],
            )
        elif event_type == "APPOINTMENT_MODIFY":
            updated_appointment = json.loads(request.body)["object"]
            defaults = {
                "api_id": updated_appointment["id"],
                "doctor_id": updated_appointment["doctor"],
                "patient_id": updated_appointment["patient"],
                "exam_room": updated_appointment["exam_room"],
                "is_walk_in": updated_appointment["is_walk_in"],
                "scheduled_time": updated_appointment["scheduled_time"],
                "status": updated_appointment["status"],
                "reason": updated_appointment["reason"],
            }
            if updated_appointment["status"] == "Arrived":
                defaults["check_in_time"] = timezone.now()
            Appointment.objects.update_or_create(
                api_id=updated_appointment["id"], defaults=defaults
            )
        elif event_type == "PATIENT_CREATE":
            new_patient = json.loads(request.body)["object"]
            Patient.objects.create(
                api_id=new_patient["id"],
                doctor_id=new_patient["doctor"],
                first_name=new_patient["first_name"],
                middle_name=new_patient["middle_name"],
                last_name=new_patient["last_name"],
                date_of_first_appointment=new_patient["date_of_first_appointment"],
                address=new_patient["address"],
                city=new_patient["city"],
                state=new_patient["state"],
                zip_code=new_patient["zip_code"],
                gender=new_patient["gender"],
                ethnicity=new_patient["ethnicity"],
                social_security_number=new_patient["social_security_number"],
                date_of_birth=new_patient["date_of_birth"],
            )
        elif event_type == "PATIENT_MODIFY":
            updated_patient = json.loads(request.body)["object"]
            Patient.objects.update_or_create(
                api_id=updated_patient["id"],
                defaults={
                    "doctor_id": updated_patient["doctor"],
                    "first_name": updated_patient["first_name"],
                    "middle_name": updated_patient["middle_name"],
                    "last_name": updated_patient["last_name"],
                    "date_of_first_appointment": updated_patient[
                        "date_of_first_appointment"
                    ],
                    "address": updated_patient["address"],
                    "city": updated_patient["city"],
                    "state": updated_patient["state"],
                    "zip_code": updated_patient["zip_code"],
                    "gender": updated_patient["gender"],
                    "ethnicity": updated_patient["ethnicity"],
                    "social_security_number": updated_patient["social_security_number"],
                    "date_of_birth": updated_patient["date_of_birth"],
                },
            )
        return JsonResponse({"status": "success"})
