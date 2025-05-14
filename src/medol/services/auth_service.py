from datetime import timedelta, datetime, timezone
from typing import Set, Optional

import jwt
from fastapi import HTTPException, status

from src.medol.core.config import Settings
from src.medol.core.security import verify_password
from src.medol.repositories.user_repository import UserRepository

blacklisted_tokens: Set[str] = set()


class AuthService:
    def __init__(self, session):
        self.session = session
        self.user_repo = UserRepository(session)

    async def authenticate(self, email: str, password: str) -> bool:
        user = await self.user_repo.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        return True

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(
                minutes=Settings.jwt_config().get("access_token_expire_minutes")))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, Settings.jwt_config().get("secret_key"),
                          algorithm=Settings.jwt_config().get("algorithm"))

    async def logout_token(self, token: str):
        blacklisted_tokens.add(token)

    async def verify_token(self, token: str) -> str:
        if token in blacklisted_tokens:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted")

        try:
            payload = jwt.decode(
                token,
                Settings.jwt_config().get("secret_key"),
                algorithms=[Settings.jwt_config().get("algorithm")]
            )
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

            return email

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
