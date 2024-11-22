from fastapi import Response
from app.schemas.auth_schemas import SAuthUser
from app.usecases.auth_usecase import AuthUsecase, create_access_token


class AuthService:
    def __init__(self):
            self.usecase = AuthUsecase()

    async def login_user(self, response: Response, body: SAuthUser):
        # Дописать, что возвращает функция
        user = await self.usecase.login_user(body)
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("access_token", access_token, httponly=True)
        print(access_token, type(access_token))
        return access_token
    
    async def logout_user(self, response: Response):
        response.delete_cookie("access_token")
        