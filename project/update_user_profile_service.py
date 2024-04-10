from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    """
    Confirms the successful update of the user's profile along with a summary of the updated fields.
    """

    userId: str
    updatedFields: List[str]
    message: str


async def update_user_profile(
    userId: str,
    firstName: Optional[str],
    lastName: Optional[str],
    email: Optional[str],
    timeZone: Optional[str],
) -> UpdateUserProfileResponse:
    """
    Updates the profile of the authenticated user.

    Args:
      userId (str): The unique identifier of the user whose profile is to be updated.
      firstName (Optional[str]): The first name of the user.
      lastName (Optional[str]): The last name of the user.
      email (Optional[str]): The email address of the user.
      timeZone (Optional[str]): The preferred time zone of the user.

    Returns:
      UpdateUserProfileResponse: Confirms the successful update of the user's profile along with a summary of the updated fields.
    """
    updated_fields = []
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        raise ValueError("No user found with the given userId")
    if email and user.email != email:
        await prisma.models.User.prisma().update(
            where={"id": userId}, data={"email": email}
        )
        updated_fields.append("email")
    profile = await prisma.models.Profile.prisma().find_unique(where={"userId": userId})
    if profile:
        update_data = {}
        if firstName and profile.firstName != firstName:
            update_data["firstName"] = firstName
            updated_fields.append("firstName")
        if lastName and profile.lastName != lastName:
            update_data["lastName"] = lastName
            updated_fields.append("lastName")
        if timeZone and profile.timeZone != timeZone:
            update_data["timeZone"] = timeZone
            updated_fields.append("timeZone")
        if update_data:
            await prisma.models.Profile.prisma().update(
                where={"userId": userId}, data=update_data
            )
    return UpdateUserProfileResponse(
        userId=userId,
        updatedFields=updated_fields,
        message="User profile updated successfully",
    )
