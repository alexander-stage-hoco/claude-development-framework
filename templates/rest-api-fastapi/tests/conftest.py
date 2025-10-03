"""
Pytest Configuration and Fixtures

Shared test fixtures for unit, integration, and BDD tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.db.database import Base, get_db
from src.models.user import User
from src.services.user_service import UserService
from src.models.schemas import UserCreate


# Test database setup (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database for each test.

    Yields:
        SQLAlchemy Session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create test client with test database.

    Args:
        db_session: Test database session

    Returns:
        FastAPI TestClient
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """
    Sample user creation data.

    Returns:
        UserCreate schema
    """
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="TestPassword123!",
    )


@pytest.fixture
def created_user(db_session, sample_user_data):
    """
    Create a user in the test database.

    Args:
        db_session: Test database session
        sample_user_data: User creation data

    Returns:
        Created User model
    """
    user_service = UserService(db_session)
    user = user_service.create_user(sample_user_data)
    return user


@pytest.fixture
def auth_headers(client, created_user):
    """
    Get authentication headers with JWT token.

    Args:
        client: Test client
        created_user: Created user

    Returns:
        Headers dict with Authorization bearer token
    """
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": created_user.username,
            "password": "TestPassword123!",  # From sample_user_data
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
