from uuid import UUID

from fastapi import HTTPException

from app.schemas.user_schemas import SCreateUser, SShowUser, SUpdateUserRequest
from app.usecases.user_usecase import UserUsecase


class UserService:
    def __init__(self, usecase: UserUsecase):
        self.usecase = usecase

            
    async def create_user(
        self, 
        body: SCreateUser,
        ) -> SShowUser:
        if await self.usecase.get_user_info_by_factory_employee_id(body.factory_employee_id):
            raise HTTPException(
                status_code=409, 
                detail=f"User with factory employee id:{body.factory_employee_id} is already exists." 
            )
        user_id = await self.usecase.create_user_with_profile(body)
        user = await self.usecase.get_user_info_by_id(user_id)  # Для отладки. Потом убрать
        return user
     
        
    async def delete_user(
        self, 
        user_id: int,
        ) -> None:
        return await self.usecase.delete_user(user_id)
    
    
    async def get_all_users(self) -> list[SShowUser]:
        return await self.usecase.get_all_users()
    
    
    async def get_user_info_by_factory_employee_id(
        self, 
        factory_employee_id: int,
        ) -> SShowUser:
        return await self.usecase.get_user_info_by_factory_employee_id(factory_employee_id)
    
    
    async def update_user(self, body: SUpdateUserRequest, user_id: UUID):
        return await self.usecase.update_user(body, user_id)
