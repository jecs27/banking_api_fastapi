import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.models.base import Base
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.schemas.user_schemas import UserCreate, UserUpdate

# Configuración de la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    repo = UserRepository(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User"
    )
    
    user = repo.create(user_data)
    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"

def test_get_user_by_email(db_session):
    repo = UserRepository(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User"
    )
    
    created_user = repo.create(user_data)
    fetched_user = repo.get_by_email("test@example.com")
    
    assert fetched_user is not None
    assert fetched_user.email == created_user.email

def test_update_user(db_session):
    repo = UserRepository(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User"
    )
    
    user = repo.create(user_data)
    update_data = UserUpdate(
        email="user@example.com",
        first_name="Updated",
        last_name="Name"
    )
    
    updated_user = repo.update(user.id, update_data)
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"