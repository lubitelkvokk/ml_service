from src.repositories.UserRepository import user_repository
from src.schemas.user import User
from src.exceptions import UserNotFoundError
from src.schemas.predictor import Predictior
from src.repositories.ModelRepository import model_repository


class UserService:

    async def check_balance(self, user: User) -> int:
        user_info = await user_repository.get_by_id(id=user.id)
        if user_info is None:
            raise UserNotFoundError()
        return user_info.balance

    async def add_model(self, model: Predictior):
        await model_repository.add(model.dict())

    async def get_all_models(self):
        models = await model_repository.list_all()
        return models

user_service = UserService()