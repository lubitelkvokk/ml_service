from passlib.context import CryptContext
from src.repositories.UserRepository import UserRepository
from src.schemas.auth import UserCreate, SignInResponse, UserLogin
from src.schemas.user import User
from src.exceptions import UserExists, UserNotFoundError, InvalidPassword
from src.core.security import security
import datetime


class SecurityService:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user_repository = UserRepository()

    async def create_user_payload(self, user_info):
        return {
            'user_id': user_info.id,
            'username': user_info.username,
            'email': user_info.email,
            'dev': user_info.developer
        }

    async def create_sign_in_response(self, user_info):
        payload = await self.create_user_payload(user_info)
        access_token = security.create_access_token(payload, user_info.developer)
        current_datetime = datetime.datetime.now().isoformat()
        user = User(id=user_info.id, username=user_info.username, email=user_info.email, dev=user_info.developer)
        return SignInResponse(access_token=access_token, expiration=current_datetime, user_info=user)

    async def sign_up(self, user: UserCreate):
        user_db_info = await self.user_repository.get_by_username(username=user.username)

        if user_db_info is not None:
            raise UserExists()

        hashed_password = self.password_context.hash(user.password)
        new_user = await self.user_repository.add({
            "username": user.username,
            "hashed_password": hashed_password,
            "email": user.email,
            'developer': user.dev
        })

        new_user = await self.user_repository.get_by_username(username=user.username)

        return await self.create_sign_in_response(new_user)

    async def sign_in(self, user: UserLogin):
        user_db_info = await self.user_repository.get_by_username(username=user.username)

        if user_db_info is None:
            raise UserNotFoundError()

        if not self.password_context.verify(user.password, user_db_info.hashed_password):
            raise InvalidPassword()

        return await self.create_sign_in_response(user_db_info)


security_service = SecurityService()
