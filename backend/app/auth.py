from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
from typing import Optional
from .database import User, Session as DBSession

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    """Hash a password using bcrypt

    Note: bcrypt has a maximum password length of 72 bytes.
    We truncate to 72 characters (assuming ASCII, 1 char = 1 byte)
    to prevent errors with very long passwords.
    """
    # Truncate password to 72 characters to prevent bcrypt errors
    # bcrypt maximum is 72 bytes, so we limit to 72 chars to be safe
    if len(password) > 72:
        password = password[:72]

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash

    Note: Applies same 72-character truncation as hash_password
    to ensure consistent password verification.
    """
    # Apply same truncation as hash_password
    if len(plain_password) > 72:
        plain_password = plain_password[:72]

    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_session(user_id: str, db: Session) -> str:
    """Create a session in database and return token"""
    token = create_access_token(user_id)
    expires_at = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    db_session = DBSession(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return token

def verify_session(token: str, db: Session) -> Optional[User]:
    """Verify session token and return user"""
    # Check token in database
    db_session = db.query(DBSession).filter(DBSession.token == token).first()
    
    if not db_session:
        return None
    
    # Check if expired
    if db_session.expires_at < datetime.utcnow():
        db.delete(db_session)
        db.commit()
        return None
    
    # Get user
    user = db.query(User).filter(User.id == db_session.user_id).first()
    return user

def delete_session(token: str, db: Session) -> bool:
    """Delete a session (logout)"""
    db_session = db.query(DBSession).filter(DBSession.token == token).first()
    if db_session:
        db.delete(db_session)
        db.commit()
        return True
    return False