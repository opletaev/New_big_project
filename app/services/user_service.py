from app.schemas.user_schemas import SCreateUser, SUpdateUserRequest
from app.usecases.user_usecase import UserUsecase


class UserService:
    def __init__(self):
            self.usecase = UserUsecase()
            
    async def register_user(self, body: SCreateUser):
        # Cделать проверку на существование пользователя
        return await self.usecase.create_user(body)
    
    async def delete_user(self, user_id: int):
        return await self.usecase.delete_user(user_id)
    
    async def get_user_by_factory_employee_id(self, factory_employee_id: int):
        return await self.usecase.get_user_by_factory_employee_id(factory_employee_id)
    
    async def update_user(self, body: SUpdateUserRequest):
        return await self.usecase.update_user(body)
