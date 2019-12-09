from drchrono.models import Appointment


def get_average_wait_time():
    appointments = Appointment.today.filter(final_wait_time__isnull=False)
    wait_times = [appointment.final_wait_time for appointment in appointments]
    if wait_times:
        return int(sum(wait_times) / len(wait_times))
    else:
        return 0
