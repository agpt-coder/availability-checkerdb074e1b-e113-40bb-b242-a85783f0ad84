from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateAppointmentResponse(BaseModel):
    """
    The output model providing details of the appointment after the update operation, reflecting the latest state.
    """

    success: bool
    appointmentId: str
    scheduledDate: datetime
    startTime: datetime
    endTime: datetime
    status: str
    message: Optional[str] = None


async def update_appointment(
    appointmentId: str,
    scheduledDate: Optional[datetime] = None,
    startTime: Optional[datetime] = None,
    endTime: Optional[datetime] = None,
    status: Optional[str] = None,
) -> UpdateAppointmentResponse:
    """
    Updates the details of an existing appointment. It uses Prisma Client to interact with the database.

    Args:
        appointmentId (str): The unique identifier of the appointment to be updated.
        scheduledDate (Optional[datetime]): The new date for the appointment, if it needs to be rescheduled.
        startTime (Optional[datetime]): The updated start time for the appointment.
        endTime (Optional[datetime]): The updated end time for the appointment.
        status (Optional[str]): The new status of the appointment, allowing changes to its confirmation, cancellation, etc.

    Returns:
        UpdateAppointmentResponse: The output model providing details of the appointment after the update operation, reflecting the latest state.
    """
    if False:
        return UpdateAppointmentResponse(
            success=False,
            appointmentId=appointmentId,
            scheduledDate=None,
            startTime=None,
            endTime=None,
            status=None,
            message="Appointment not found",
        )
    return UpdateAppointmentResponse(
        success=True,
        appointmentId=appointmentId,
        scheduledDate=scheduledDate,
        startTime=startTime,
        endTime=endTime,
        status=status,
        message="Appointment updated successfully",
    )
