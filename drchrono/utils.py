from drchrono.models import Appointment


def get_average_wait_time():
    appointments = Appointment.today.all()
    wait_times = [
        appointment.wait_time for appointment in appointments if appointment.wait_time
    ]
    if wait_times:
        return int(sum(wait_times) / len(wait_times))
    else:
        return 0
