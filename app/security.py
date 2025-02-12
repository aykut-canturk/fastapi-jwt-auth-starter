from datetime import datetime, timedelta, UTC
from contextvars import ContextVar
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.config import jwt_settings
from app.models.user import Users

bearer = HTTPBearer()

current_user_id: ContextVar[Optional[int]] = ContextVar("current_user_id", default=None)


async def _get_jwt_payload(token: str) -> Dict[str, Any]:
    """
    Decodes and returns the JWT payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            jwt_settings.authjwt_secret_key,
            algorithms=[jwt_settings.authjwt_algorithm],
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return payload


async def _verify_token_type(
    credentials: HTTPAuthorizationCredentials, expected_type: str
) -> str:
    """
    Verifies that the provided JWT has the expected token type.

    Args:
        credentials: The HTTP credentials containing the JWT.
        expected_type: The token type expected ("access" or "refresh").

    Returns:
        The subject ("sub") claim from the token.

    Raises:
        HTTPException: If the token type does not match the expected type.
    """
    payload = await _get_jwt_payload(credentials.credentials)
    token_type = payload.get("type")
    if token_type != expected_type:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid token type. {expected_type} token required",
        )
    return payload.get("sub")


async def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    """
    Dependency that verifies an access token and returns the subject.
    """
    return await _verify_token_type(credentials, "access")


async def verify_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> str:
    """
    Dependency that verifies a refresh token and returns the subject.
    """
    return await _verify_token_type(credentials, "refresh")


def _create_jwt_token(user: Users, token_type: str) -> str:
    """
    Creates a JWT for the given user and token type.

    Args:
        user: The user object.
        token_type: The type of token to create ("access" or "refresh").

    Returns:
        A JWT as a string.

    Raises:
        ValueError: If an unsupported token type is provided.
    """
    now = datetime.now(UTC)
    if token_type == "access":
        exp = now + timedelta(minutes=jwt_settings.access_token_expire_minutes)
    elif token_type == "refresh":
        exp = now + timedelta(days=jwt_settings.refresh_token_expire_days)
    else:
        raise ValueError("Invalid token type provided. Expected 'access' or 'refresh'.")

    payload = {
        "sub": str(user.id),
        "type": token_type,
        "iat": now,
        "exp": exp,
        "email": user.email,
    }

    return jwt.encode(
        payload,
        jwt_settings.authjwt_secret_key,
        algorithm=jwt_settings.authjwt_algorithm,
    )


async def create_access_token(user: Users) -> str:
    """
    Creates an access token for the given user.
    """
    return _create_jwt_token(user, "access")


async def create_refresh_token(user: Users) -> str:
    """
    Creates a refresh token for the given user.
    """
    return _create_jwt_token(user, "refresh")


async def _get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extracts the user ID from the JWT.

    Args:
        token: The JWT token.

    Returns:
        The user ID as an integer if available, otherwise None.
    """
    payload = await _get_jwt_payload(token)
    sub = payload.get("sub")
    return int(sub) if sub is not None else None


async def set_current_user_id(token: str) -> None:
    """
    Sets the current user ID from the provided token in the ContextVar.
    """
    try:
        user_id = await _get_user_id_from_token(token)
    except Exception:
        user_id = None
    current_user_id.set(user_id)


def get_current_user_id() -> Optional[int]:
    """
    Retrieves the current user ID from the ContextVar.
    """
    return current_user_id.get()
