from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import get_db_session
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate, UserLogin, UserResponse
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def _get_service(session: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(repo=AuthRepository(session))


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: UserCreate, service: AuthService = Depends(_get_service)):
    user = await service.register_user(payload)
    return user


@router.post("/login")
async def login(payload: UserLogin, service: AuthService = Depends(_get_service)):
    user = await service.login_user(payload)
    return user


@router.get("/me", response_model=UserResponse)
async def me(service: AuthService = Depends(_get_service)):
    # TODO: extract user_id from JWT token
    user = await service.get_current_user("placeholder-user-id")
    return user
