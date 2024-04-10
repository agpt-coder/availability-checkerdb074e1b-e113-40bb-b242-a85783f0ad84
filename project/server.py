import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import project.book_appointment_service
import project.cancel_appointment_service
import project.get_user_profile_service
import project.login_user_service
import project.register_user_service
import project.update_appointment_service
import project.update_user_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Availability Checker",
    lifespan=lifespan,
    description="To achieve the functionality of returning real-time availability of professionals and updating based on current activity or schedule, the following steps and best practices should be implemented using the selected tech stack: Python, FastAPI, PostgreSQL, and Prisma. \n\n1. **System Design:** Create a microservice architecture where the scheduling logic resides in one service that communicates with other services (e.g., user management, calendar service) through RESTful APIs or message brokers. This separation of concerns enhances scalability and maintainability.\n\n2. **FastAPI Implementation:** Use FastAPI to handle incoming HTTP requests related to scheduling. FastAPI's async capabilities allow for efficient real-time processing of requests, making it well-suited for operations that require immediate feedback on professionals' availability.\n\n3. **Real-time Communication:** Implement WebSocket in FastAPI for real-time communication between the client and server. This is crucial for notifying clients about immediate changes in professionals' availability.\n\n4. **Database Management with Prisma:** Utilize PostgreSQL for storing professionals' schedules and availability. Prisma serves as the ORM, simplifying database transactions and ensuring efficient, asynchronous access to data. The `PrismaClient` allows for easy querying and real-time updates.\n\n5. **Scheduling Logic:** Develop a robust scheduling algorithm that considers professionals' current activities, preferences, and time-offs. This algorithm should dynamically update availability as appointments are booked or cancelled.\n\n6. **User Interfaces:** Create user-friendly interfaces for professionals to manage their schedules and availability. Similarly, clients should have an intuitive interface to view real-time availability and book appointments.\n\n7. **Notification System:** Implement a notification system, using FastAPI's BackgroundTasks, to alert professionals and clients of new bookings, cancellations, or changes in the schedule. This enhances the user experience by keeping all parties informed in real-time.\n\n8. **Security and Authentication:** Secure API endpoints using FastAPI's security utilities to ensure that access to professionals' schedules and personal data is restricted to authenticated users only.\n\n9. **Scaling and Optimization:** Monitor system performance and optimize as needed. This includes database indexing, query optimization, and considering a microservices architecture for horizontal scaling.\n\n10. **Documentation and Testing:** Write comprehensive documentation for the API, detailing endpoints, usage, and examples. Implement thorough testing strategies, including unit and integration tests, to ensure reliability and identify issues pre-deployment.\n\nBy meticulously following these guidelines and leveraging the power of the chosen tech stack, you can successfully implement a system that accurately reflects real-time availability of professionals, enhancing both operational efficiency and user satisfaction.",
)


@app.put(
    "/users/profile/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    userId: str,
    firstName: Optional[str],
    lastName: Optional[str],
    email: Optional[str],
    timeZone: Optional[str],
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Updates the profile of the authenticated user.
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            userId, firstName, lastName, email, timeZone
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/appointments/cancel/{appointmentId}",
    response_model=project.cancel_appointment_service.CancelAppointmentResponse,
)
async def api_patch_cancel_appointment(
    appointmentId: str,
) -> project.cancel_appointment_service.CancelAppointmentResponse | Response:
    """
    Allows a client to cancel an existing appointment.
    """
    try:
        res = await project.cancel_appointment_service.cancel_appointment(appointmentId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    email: str, password: str, first_name: str, last_name: str, time_zone: str
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Registers a new user and creates their profile.
    """
    try:
        res = await project.register_user_service.register_user(
            email, password, first_name, last_name, time_zone
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/appointments/book",
    response_model=project.book_appointment_service.BookAppointmentResponse,
)
async def api_post_book_appointment(
    clientId: str,
    professionalId: str,
    appointmentDate: str,
    startTime: str,
    endTime: str,
) -> project.book_appointment_service.BookAppointmentResponse | Response:
    """
    Allows a client to book an appointment with a professional.
    """
    try:
        res = await project.book_appointment_service.book_appointment(
            clientId, professionalId, appointmentDate, startTime, endTime
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/profile",
    response_model=project.get_user_profile_service.UserProfileResponse,
)
async def api_get_get_user_profile() -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieves the profile of the authenticated user.
    """
    try:
        res = await project.get_user_profile_service.get_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/appointments/update/{appointmentId}",
    response_model=project.update_appointment_service.UpdateAppointmentResponse,
)
async def api_put_update_appointment(
    appointmentId: str,
    scheduledDate: Optional[datetime],
    startTime: Optional[datetime],
    endTime: Optional[datetime],
    status: Optional[str],
) -> project.update_appointment_service.UpdateAppointmentResponse | Response:
    """
    Updates the details of an existing appointment.
    """
    try:
        res = await project.update_appointment_service.update_appointment(
            appointmentId, scheduledDate, startTime, endTime, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/login", response_model=project.login_user_service.LoginResponse)
async def api_post_login_user(
    email: str, password: str
) -> project.login_user_service.LoginResponse | Response:
    """
    Authenticates user credentials and returns an access token.
    """
    try:
        res = await project.login_user_service.login_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
