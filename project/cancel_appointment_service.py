from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CancelAppointmentResponse(BaseModel):
    """
    Outputs the result of the cancellation operation, including a confirmation message and the cancelled appointment's updated status.
    """

    message: str
    appointmentId: str
    status: str


async def cancel_appointment(appointmentId: str) -> CancelAppointmentResponse:
    """
    Allows a client to cancel an existing appointment.

    This function first checks if the appointment with the given ID exists. If it does, it updates the
    appointment's status to "Cancelled" and returns a confirmation response. If the appointment doesn't exist or
    an error occurs during the process, it returns an appropriate error message.

    Args:
        appointmentId (str): The unique identifier of the appointment to be cancelled.

    Returns:
        CancelAppointmentResponse: Outputs the result of the cancellation operation, including a confirmation message and the cancelled appointment's updated status.
    """
    appointment = await prisma.models.Appointment.prisma().find_unique(
        where={"id": appointmentId}
    )
    if not appointment:
        return CancelAppointmentResponse(
            message="prisma.models.Appointment not found.",
            appointmentId=appointmentId,
            status="Failed",
        )
    if appointment.status == "Cancelled":
        return CancelAppointmentResponse(
            message="The appointment is already cancelled.",
            appointmentId=appointmentId,
            status="Cancelled",
        )
    updated_appointment = await prisma.models.Appointment.prisma().update(
        where={"id": appointmentId},
        data={"status": "Cancelled", "updatedAt": datetime.now()},
    )
    response = CancelAppointmentResponse(
        message="prisma.models.Appointment cancelled successfully.",
        appointmentId=appointmentId,
        status=updated_appointment.status,
    )
    return response
