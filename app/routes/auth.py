from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.database import SessionDep
from app.services.user import get_user_service
from app.schemas.user import UserLogin
from app.security import create_access_token, create_refresh_token, verify_refresh_token

router = APIRouter()


@router.post("/login")
async def login(user: UserLogin, session: SessionDep):
    user = get_user_service(session).login(user.email, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh(
    session: SessionDep,
    user_id: Annotated[str, Depends(verify_refresh_token)],
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    user = get_user_service(session).get(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    access_token = await create_access_token(user)
    return {"access_token": access_token}
