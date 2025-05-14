from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.medol.db.config import get_async_session
from src.medol.dependencies.dependencies import oauth2_scheme
from src.medol.schemas.token_schema import Token
from src.medol.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        auth_service = AuthService(session)

    if not await auth_service.authenticate(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await auth_service.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        auth_service = AuthService(session)

    await auth_service.logout_token(token)
    return {"message": "Successfully logged out"}
