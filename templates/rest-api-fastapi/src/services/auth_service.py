"""
Authentication Service

Business logic for authentication and JWT token management.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.config import settings
from src.models.user import User
from src.models.schemas import TokenData
from src.services.user_service import UserService


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class InvalidTokenError(Exception):
    """Raised when token is invalid."""

    pass


class AuthService:
    """
    Authentication service.

    Handles JWT token generation, validation, and user authentication.
    """

    def __init__(self, db: Session):
        """
        Initialize auth service.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.user_service = UserService(db)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username/email and password.

        Args:
            username: Username or email
            password: Plain text password

        Returns:
            User if authentication successful, None otherwise
        """
        # Try to find user by username
        user = self.user_service.get_user_by_username(username)

        # If not found, try email
        if not user:
            user = self.user_service.get_user_by_email(username)

        # Check password
        if not user:
            return None

        if not UserService.verify_password(password, user.hashed_password):
            return None

        return user

    def create_access_token(
        self,
        user: User,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create JWT access token for user.

        Args:
            user: User to create token for
            expires_delta: Optional custom expiration time

        Returns:
            JWT token string
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": user.username,
            "user_id": str(user.id),
            "exp": expire,
        }

        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt

    def decode_token(self, token: str) -> TokenData:
        """
        Decode and validate JWT token.

        Args:
            token: JWT token string

        Returns:
            TokenData with user information

        Raises:
            InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")

            if username is None:
                raise InvalidTokenError("Invalid token payload")

            return TokenData(
                username=username,
                user_id=UUID(user_id) if user_id else None,
            )
        except JWTError as e:
            raise InvalidTokenError(f"Token validation failed: {str(e)}")

    def get_current_user(self, token: str) -> User:
        """
        Get current user from JWT token.

        Args:
            token: JWT token string

        Returns:
            User

        Raises:
            InvalidTokenError: If token is invalid
            AuthenticationError: If user not found
        """
        token_data = self.decode_token(token)

        user = None
        if token_data.username:
            user = self.user_service.get_user_by_username(token_data.username)

        if user is None:
            raise AuthenticationError("User not found")

        return user
