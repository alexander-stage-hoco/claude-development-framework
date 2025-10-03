"""
User Service

Business logic for user management operations.
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.models.user import User
from src.models.schemas import UserCreate, UserUpdate


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAlreadyExistsError(Exception):
    """Raised when user with email or username already exists."""

    pass


class UserNotFoundError(Exception):
    """Raised when user is not found."""

    pass


class UserService:
    """
    User service for business logic operations.

    Handles user CRUD operations with proper validation and error handling.
    """

    def __init__(self, db: Session):
        """
        Initialize user service.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user

        Raises:
            UserAlreadyExistsError: If email or username already exists
        """
        # Check if email exists (case-insensitive)
        existing_user = self.db.query(User).filter(User.email.ilike(user_data.email)).first()
        if existing_user:
            raise UserAlreadyExistsError("Email already registered")

        # Check if username exists
        existing_user = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise UserAlreadyExistsError("Username already exists")

        # Hash password
        hashed_password = pwd_context.hash(user_data.password)

        # Create user
        db_user = User(
            email=user_data.email.lower(),  # Store email in lowercase
            username=user_data.username,
            hashed_password=hashed_password,
        )

        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsError("User already exists")

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email (case-insensitive).

        Args:
            email: User email

        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.email.ilike(email)).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username

        Returns:
            User or None if not found
        """
        return self.db.query(User).filter(User.username == username).first()

    def list_users(self, skip: int = 0, limit: int = 10) -> tuple[List[User], int]:
        """
        List users with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of users, total count)
        """
        total = self.db.query(User).count()
        users = self.db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
        return users, total

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        """
        Update user.

        Args:
            user_id: User ID
            user_update: Update data

        Returns:
            Updated user

        Raises:
            UserNotFoundError: If user not found
            UserAlreadyExistsError: If email/username conflicts
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        # Update fields if provided
        if user_update.email is not None:
            # Check email uniqueness
            existing = self.get_user_by_email(user_update.email)
            if existing and existing.id != user_id:
                raise UserAlreadyExistsError("Email already registered")
            user.email = user_update.email.lower()

        if user_update.username is not None:
            # Check username uniqueness
            existing = self.get_user_by_username(user_update.username)
            if existing and existing.id != user_id:
                raise UserAlreadyExistsError("Username already exists")
            user.username = user_update.username

        if user_update.password is not None:
            user.hashed_password = pwd_context.hash(user_update.password)

        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise UserAlreadyExistsError("User data conflicts with existing user")

    def delete_user(self, user_id: UUID) -> bool:
        """
        Delete user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches
        """
        return pwd_context.verify(plain_password, hashed_password)
