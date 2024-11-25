from fastapi import Response
from app.schemas.auth_schemas import SAuthUser
from app.usecases.auth_usecase import AuthUsecase, create_access_token


class AuthService:
    def __init__(self, usecase: AuthUsecase):
            self.usecase = usecase
            
    async def login_user(
        self, 
        response: Response, 
        body: SAuthUser
        ) -> str:
        user_id = await self.usecase.check_user(body)
        access_token = create_access_token({"sub": str(user_id)})
        response.set_cookie("access_token", access_token, httponly=True)
        print(access_token, type(access_token))
        return access_token
    
    
    async def logout_user(
        self, 
        response: Response
        ) -> None:
        response.delete_cookie("access_token")
        