import pytest
from datetime import timedelta
from jose import jwt
from src.infrastructure.config.settings import settings
from src.application.services.auth_service import AuthService
from src.infrastructure.repositories.user_repository import UserRepository

class MockUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
    
    def get_by_email(self, email: str):
        return self.users.get(email)

def test_create_access_token():
    user_repo = MockUserRepository()
    auth_service = AuthService(user_repo)
    
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    
    token = auth_service.create_access_token(data, expires_delta)
    
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == "test@example.com"

def test_verify_token():
    user_repo = MockUserRepository()
    auth_service = AuthService(user_repo)
    
    # Create a token
    token = auth_service.create_access_token({"sub": "test@example.com"})
    
    # Verify the token
    token_data = auth_service.verify_token(token)
    assert token_data.email == "test@example.com"