"""
User API Endpoints

REST endpoints for user management (CRUD operations).
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_current_user
from src.models.user import User
from src.models.schemas import UserCreate, UserResponse, UserUpdate, UserList
from src.services.user_service import (
    UserService,
    UserAlreadyExistsError,
    UserNotFoundError,
)

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    - **email**: User email (unique)
    - **username**: Username (unique, 3-50 chars, alphanumeric/-/_)
    - **password**: Password (minimum 8 characters)

    Returns created user (without password).
    """
    user_service = UserService(db)

    try:
        user = user_service.create_user(user_data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=UserList)
def list_users(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Authentication required
):
    """
    List users with pagination.

    Requires authentication.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 10, max: 100)

    Returns paginated list of users.
    """
    user_service = UserService(db)
    users, total = user_service.list_users(skip=skip, limit=limit)

    return UserList(
        items=users,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Authentication required
):
    """
    Get user by ID.

    Requires authentication.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Authentication required
):
    """
    Update user.

    Requires authentication. Users can only update their own profile.
    """
    # Check authorization: users can only update their own profile
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user_service = UserService(db)

    try:
        user = user_service.update_user(user_id, user_update)
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Authentication required
):
    """
    Delete user.

    Requires authentication. Users can only delete their own account.
    """
    # Check authorization: users can only delete their own account
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    user_service = UserService(db)
    deleted = user_service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return None  # 204 No Content
