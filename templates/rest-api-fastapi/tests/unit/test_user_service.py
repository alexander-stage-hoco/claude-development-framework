"""
Unit Tests for UserService

Tests for user service business logic (isolated from API layer).
"""

import pytest
from src.services.user_service import (
    UserService,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models.schemas import UserCreate, UserUpdate


def test_create_user_success(db_session, sample_user_data):
    """Test successful user creation."""
    user_service = UserService(db_session)

    user = user_service.create_user(sample_user_data)

    assert user.id is not None
    assert user.email == sample_user_data.email.lower()
    assert user.username == sample_user_data.username
    assert user.hashed_password is not None
    assert user.hashed_password != sample_user_data.password  # Password should be hashed


def test_create_user_duplicate_email(db_session, created_user, sample_user_data):
    """Test that duplicate email raises error."""
    user_service = UserService(db_session)

    # Try to create user with same email
    duplicate_data = UserCreate(
        email=created_user.email,
        username="different_username",
        password="DifferentPass123!",
    )

    with pytest.raises(UserAlreadyExistsError, match="Email already registered"):
        user_service.create_user(duplicate_data)


def test_create_user_duplicate_username(db_session, created_user):
    """Test that duplicate username raises error."""
    user_service = UserService(db_session)

    # Try to create user with same username
    duplicate_data = UserCreate(
        email="different@example.com",
        username=created_user.username,
        password="DifferentPass123!",
    )

    with pytest.raises(UserAlreadyExistsError, match="Username already exists"):
        user_service.create_user(duplicate_data)


def test_get_user_by_id(db_session, created_user):
    """Test retrieving user by ID."""
    user_service = UserService(db_session)

    user = user_service.get_user_by_id(created_user.id)

    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email


def test_get_user_by_email_case_insensitive(db_session, created_user):
    """Test that email lookup is case-insensitive."""
    user_service = UserService(db_session)

    # Try different cases
    user1 = user_service.get_user_by_email(created_user.email.upper())
    user2 = user_service.get_user_by_email(created_user.email.lower())
    user3 = user_service.get_user_by_email(created_user.email.title())

    assert user1 is not None
    assert user2 is not None
    assert user3 is not None
    assert user1.id == user2.id == user3.id


def test_list_users_pagination(db_session):
    """Test user listing with pagination."""
    user_service = UserService(db_session)

    # Create multiple users
    for i in range(15):
        user_data = UserCreate(
            email=f"user{i}@example.com",
            username=f"user{i}",
            password=f"Password{i}!",
        )
        user_service.create_user(user_data)

    # Test pagination
    users, total = user_service.list_users(skip=0, limit=10)
    assert len(users) == 10
    assert total == 15

    users, total = user_service.list_users(skip=10, limit=10)
    assert len(users) == 5
    assert total == 15


def test_update_user(db_session, created_user):
    """Test updating user information."""
    user_service = UserService(db_session)

    update_data = UserUpdate(
        email="newemail@example.com",
        username="newusername",
    )

    updated_user = user_service.update_user(created_user.id, update_data)

    assert updated_user.email == "newemail@example.com"
    assert updated_user.username == "newusername"


def test_delete_user(db_session, created_user):
    """Test user deletion."""
    user_service = UserService(db_session)

    # Delete user
    result = user_service.delete_user(created_user.id)
    assert result is True

    # Verify user is deleted
    user = user_service.get_user_by_id(created_user.id)
    assert user is None


def test_verify_password(db_session, sample_user_data):
    """Test password verification."""
    user_service = UserService(db_session)

    # Create user
    user = user_service.create_user(sample_user_data)

    # Verify correct password
    assert UserService.verify_password(sample_user_data.password, user.hashed_password) is True

    # Verify incorrect password
    assert UserService.verify_password("WrongPassword", user.hashed_password) is False
