"""
Authentication API Endpoints

REST endpoints for user authentication (login, token management).
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.config import settings
from src.models.schemas import LoginRequest, Token
from src.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT access token.

    - **username**: Username or email
    - **password**: User password

    Returns JWT token for authenticated requests.

    Example:
        ```json
        {
            "username": "johndoe",
            "password": "SecurePass123!"
        }
        ```

    Response:
        ```json
        {
            "access_token": "eyJhbGci...",
            "token_type": "bearer",
            "expires_in": 3600
        }
        ```
    """
    auth_service = AuthService(db)

    # Authenticate user
    user = auth_service.authenticate_user(
        username=login_data.username,
        password=login_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        user=user,
        expires_delta=access_token_expires,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
    )
