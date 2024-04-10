from datetime import datetime

import prisma
import prisma.enums
import prisma.models
import pytz
from pydantic import BaseModel


class BookAppointmentResponse(BaseModel):
    """
    Confirms the details of the booked appointment including identifiers and timing.
    """

    appointmentId: str
    clientId: str
    professionalId: str
    appointmentDate: str
    startTime: str
    endTime: str
    status: str


async def book_appointment(
    clientId: str,
    professionalId: str,
    appointmentDate: str,
    startTime: str,
    endTime: str,
) -> BookAppointmentResponse:
    """
    Allows a client to book an appointment with a professional.
    This function first checks the availability of the professional for the given date and time,
    then books an appointment if possible, and finally returns the details of the appointment.

    Args:
        clientId (str): Unique identifier for the client booking the appointment.
        professionalId (str): Unique identifier for the professional with whom the appointment is being booked.
        appointmentDate (str): The desired date for the appointment in 'YYYY-MM-DD' format.
        startTime (str): The starting time for the appointment in 'HH:MM' format.
        endTime (str): The ending time for the appointment in 'HH:MM' format.

    Returns:
        BookAppointmentResponse: Confirms the details of the booked appointment including identifiers and timing.

    Raises:
        ValueError: If the time input is invalid or if the professional is not available at the given time.
    """
    start_datetime = datetime.strptime(
        f"{appointmentDate} {startTime}", "%Y-%m-%d %H:%M"
    )
    end_datetime = datetime.strptime(f"{appointmentDate} {endTime}", "%Y-%m-%d %H:%M")
    if start_datetime >= end_datetime:
        raise ValueError("The appointment's end time must be after its start time.")
    schedules = await prisma.models.Schedule.prisma().find_many(
        where={
            "profileId": professionalId,
            "date": {"gte": start_datetime, "lte": end_datetime},
            "status": prisma.enums.ScheduleStatus.Available,
        }
    )
    if not schedules:
        raise ValueError("No available schedule found for the specified time.")
    appointment = await prisma.models.Appointment.prisma().create(
        data={
            "clientId": clientId,
            "professionalId": professionalId,
            "scheduleId": schedules[0].id,
            "createdAt": datetime.now(tz=pytz.UTC),
            "status": prisma.enums.AppointmentStatus.Pending,
        }
    )
    return BookAppointmentResponse(
        appointmentId=appointment.id,
        clientId=appointment.clientId,
        professionalId=appointment.professionalId,
        appointmentDate=appointmentDate,
        startTime=startTime,
        endTime=endTime,
        status=appointment.status,
    )
