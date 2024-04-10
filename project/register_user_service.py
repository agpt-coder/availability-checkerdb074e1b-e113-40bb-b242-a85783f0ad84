import prisma
import prisma.models
from passlib.hash import bcrypt
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    After successful registration, this model returns a confirmation message and the user's unique identifier.
    """

    success: bool
    user_id: str
    message: str


async def register_user(
    email: str, password: str, first_name: str, last_name: str, time_zone: str
) -> UserRegistrationResponse:
    """
    Registers a new user and creates their profile.

    Args:
        email (str): The email address of the new user. Will be used as the primary identifier for login.
        password (str): The password for the new user. This will be hashed before storage for security reasons.
        first_name (str): The first name of the user. Part of personal information to personalize the user profile.
        last_name (str): The last name of the user. Part of personal information to personalize the user profile.
        time_zone (str): The user's local time zone. This helps in displaying dates and times in the correct local format.

    Returns:
        UserRegistrationResponse: After successful registration, this model returns a confirmation message and the user's unique identifier.

    Example:
        register_user("john.doe@example.com", "securePassword123", "John", "Doe", "Europe/London")
        > UserRegistrationResponse(success=True, user_id="...", message="User successfully registered.")
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return UserRegistrationResponse(
            success=False, user_id="", message="A user with this email already exists."
        )
    hashed_password = bcrypt.hash(password)
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashed_password,
            "Profile": {
                "create": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "timeZone": time_zone,
                }
            },
        }
    )
    response = UserRegistrationResponse(
        success=True, user_id=user.id, message="User successfully registered."
    )
    return response
