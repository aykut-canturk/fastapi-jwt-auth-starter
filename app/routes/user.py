from fastapi import APIRouter, HTTPException
from app.models.database import SessionDep
from app.schemas.user import UserUpdate, UserCreate, UserResponse
from app.services.user import get_user_service

router = APIRouter()


def get_user_or_404(service, user_id):
    user = service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/")
async def get_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[UserResponse]:
    service = get_user_service(session)
    models = service.fetch(skip=skip, limit=limit)
    return [UserResponse.from_model(model) for model in models]


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep) -> UserResponse:
    service = get_user_service(session)
    user = get_user_or_404(service, user_id)
    return UserResponse.from_model(user)


@router.post("/")
async def create_user(user: UserCreate, session: SessionDep) -> UserResponse:
    service = get_user_service(session)
    model = service.create(user.to_model())
    return UserResponse.from_model(model)


@router.put("/{user_id}")
async def update_user(
    user_id: int, user: UserCreate, session: SessionDep
) -> UserResponse:
    service = get_user_service(session)
    model = get_user_or_404(service, user_id)
    model.first_name = user.first_name
    model.last_name = user.last_name
    model.email = user.email
    service.update(model)
    return UserResponse.from_model(model)


@router.patch("/{user_id}")
async def modify_user(
    user_id: int, user: UserUpdate, session: SessionDep
) -> UserResponse:
    service = get_user_service(session)
    model = get_user_or_404(service, user_id)
    if user.first_name:
        model.first_name = user.first_name
    if user.last_name:
        model.last_name = user.last_name
    if user.email:
        model.email = user.email
    service.update(model)
    return UserResponse.from_model(model)


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    service = get_user_service(session)
    user = get_user_or_404(service, user_id)
    service.delete(user)
    return {"message": "User deleted successfully"}
