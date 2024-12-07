from app.repositories.cable import CableRepository
from app.repositories.profile import ProfileRepository
from app.repositories.transactions import TransactionRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.cable import CableService
from app.services.debug import DebugUserService
from app.services.profile import ProfileService
from app.services.transaction import TransactionService
from app.services.user import UserService


def verify_token(request):
    return AuthService.verify_token(request)


def auth_service():
    return AuthService


def user_service():
    return UserService(UserRepository)


def profile_service():
    return ProfileService(ProfileRepository)


def cable_service():
    return CableService(CableRepository)


def transaction_service():
    return TransactionService(TransactionRepository)


def debug_user_service():
    return DebugUserService()
