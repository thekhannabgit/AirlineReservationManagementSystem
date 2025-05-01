# business_logic/auth_services.py
from hashlib import sha256
from typing import Optional, Tuple
from database.models import User, UserRole
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from config import settings

'''class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.token_expiry = settings.TOKEN_EXPIRY_MINUTES

    def register_user(self, username: str, password: str, email: str, role: UserRole = UserRole.USER) -> Tuple[bool, str]:
        """
        Register a new user with the system
        Returns tuple of (success: bool, message: str)
        """
        try:
            # Check if username exists
            if self.session.query(User).filter(User.username == username).first():
                return False, "Username already exists"

            # Check if email exists
            if self.session.query(User).filter(User.email == email).first():
                return False, "Email already registered"

            # Hash the password
            hashed_password = self._hash_password(password)

            # Create new user
            user = User(
                username=username,
                password=hashed_password,
                email=email,
                role=role,
                is_active=True
            )

            self.session.add(user)
            self.session.commit()
            return True, "Registration successful"

        except Exception as e:
            self.session.rollback()
            return False, f"Registration failed: {str(e)}"'''


class AuthService:
    def __init__(self, session):
        self.session = session

    def register_user(self, username, password, email, role=UserRole.USER):
        # Check if username exists
        if self.session.query(User).filter(User.username == username).first():
            return False, "Username already exists"

        # Check if email exists
        if self.session.query(User).filter(User.email == email).first():
            return False, "Email already registered"

        # Create new user
        user = User(
            username=username,
            password=self._hash_password(password),
            email=email,
            role=role
        )

        self.session.add(user)
        self.session.commit()
        return True, "Registration successful"

    def authenticate_user(self, username: str, password: str) -> Tuple[Optional[User], str]:
        """
        Authenticate a user with username and password
        Returns tuple of (user: Optional[User], message: str)
        """
        try:
            user = self.session.query(User).filter(User.username == username).first()

            if not user:
                return None, "Invalid username or password"

            if not user.is_active:
                return None, "Account is disabled"

            if not self._verify_password(password, user.password):
                return None, "Invalid username or password"

            return user, "Authentication successful"

        except Exception as e:
            return None, f"Authentication failed: {str(e)}"

    def generate_token(self, user: User) -> str:
        """
        Generate JWT token for authenticated user
        """
        token_data = {
            "sub": user.username,
            "role": user.role.value,
            "exp": datetime.utcnow() + timedelta(minutes=self.token_expiry)
        }
        return jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token and return payload if valid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None

    def change_password(self, user: User, current_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password after verifying current password
        Returns tuple of (success: bool, message: str)
        """
        try:
            if not self._verify_password(current_password, user.password):
                return False, "Current password is incorrect"

            user.password = self._hash_password(new_password)
            self.session.commit()
            return True, "Password changed successfully"

        except Exception as e:
            self.session.rollback()
            return False, f"Password change failed: {str(e)}"

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return sha256(password.encode()).hexdigest()

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hashed version"""
        return self._hash_password(plain_password) == hashed_password

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.session.query(User).filter(User.email == email).first()

    def create_admin_user(self):
        """Create initial admin user if not exists"""
        admin = self.session.query(User).filter(User.username == "admin").first()
        if not admin:
            self.register_user(
                username="admin",
                password="admin123",
                email="admin@skylink.com",
                role=UserRole.ADMIN
            )
            print("Admin user created successfully")