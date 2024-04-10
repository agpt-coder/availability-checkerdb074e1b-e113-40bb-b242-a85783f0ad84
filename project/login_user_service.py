from datetime import datetime, timedelta

import prisma
import prisma.models
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    The response provided after a user successfully logs in, containing the JWT token for accessing protected routes.
    """

    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password, hashed_password) -> bool:
    """
    Verifies if a plain password matches the hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    """
    Retrieves a user by their email.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        An instance of the User model if a user is found, None otherwise.
    """
    return await prisma.models.User.prisma().find_unique(where={"email": email})


async def authenticate_user(email: str, password: str):
    """
    Authenticates a user by verifying their email and password.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        The User model instance if authentication is successful, False otherwise.
    """
    user = await get_user(email)
    if not user:
        return False
    if not await verify_password(password, user.hashedPassword):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT token with a specified expiration time.

    Args:
        data (dict): The payload data of the token.
        expires_delta (timedelta, optional): The expiration time delta. Defaults to 15 minutes.

    Returns:
        str: The generated JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(email: str, password: str) -> LoginResponse:
    """
    Authenticates user credentials and returns an access token.

    Args:
        email (str): The email address of the user trying to log in.
        password (str): The password for the user which will be verified for authentication.

    Returns:
        LoginResponse: The response provided after a user successfully logs in, containing the JWT token for accessing protected routes.
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponse(access_token=access_token, token_type="bearer")
