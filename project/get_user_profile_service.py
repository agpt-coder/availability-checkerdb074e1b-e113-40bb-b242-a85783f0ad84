from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    A model that encapsulates the response data for a user profile request, containing non-sensitive profile details.
    """

    id: str
    firstName: str
    lastName: str
    email: str
    city: Optional[str] = None
    country: Optional[str] = None
    timeZone: Optional[str] = None


async def get_user_profile() -> UserProfileResponse:
    """
    Retrieves the profile of the authenticated user.

    This function assumes there's a mechanism to identify the authenticated user's ID. It fetches the user's profile details from
    the database using the Prisma Client. In a real-world application, the user's ID would typically be retrieved from
    the session or token provided with the request.

    Returns:
        UserProfileResponse: A model that encapsulates the response data for a user profile request, containing non-sensitive profile details.

    Example:
        # Assuming there's an authenticated user with specific ID
        profile = await get_user_profile()
        print(profile)
    """
    authenticated_user_id = "123e4567-e89b-12d3-a456-426614174000"
    user_data = await prisma.models.User.prisma().find_unique(
        where={"id": authenticated_user_id}, include={"Profile": True}
    )
    if not user_data or not user_data.Profile:
        raise Exception("User or user profile not found.")
    profile_response = UserProfileResponse(
        id=user_data.id,
        firstName=user_data.Profile.firstName,
        lastName=user_data.Profile.lastName,
        email=user_data.email,
        timeZone=user_data.Profile.timeZone,
    )
    return profile_response
