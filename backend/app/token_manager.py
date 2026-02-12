"""
Token management for email verification and password reset.
Handles token generation, validation, and lifecycle.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from .database import User, EmailVerificationToken, PasswordResetToken, Session as DBSession


def generate_secure_token() -> str:
    """
    Generate a cryptographically secure random token.

    Returns:
        URL-safe token string
    """
    return secrets.token_urlsafe(32)


def create_verification_token(user_id: str, db: Session) -> str:
    """
    Create an email verification token for a user.

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        Generated token string
    """
    # Invalidate any existing unused verification tokens
    existing_tokens = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.user_id == user_id,
        EmailVerificationToken.used_at.is_(None)
    ).all()

    for token in existing_tokens:
        db.delete(token)

    # Create new token (24 hour expiry)
    token = generate_secure_token()
    expires_at = datetime.utcnow() + timedelta(hours=24)

    db_token = EmailVerificationToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()

    return token


def verify_email_token(token: str, db: Session) -> Optional[User]:
    """
    Verify an email verification token and mark user as verified.

    Args:
        token: Verification token string
        db: Database session

    Returns:
        User object if verification successful, None otherwise
    """
    # Find token
    db_token = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token
    ).first()

    if not db_token:
        return None

    # Check if already used
    if db_token.used_at is not None:
        return None

    # Check if expired
    if db_token.expires_at < datetime.utcnow():
        return None

    # Get user
    user = db.query(User).filter(User.id == db_token.user_id).first()

    if not user:
        return None

    # Mark user as verified
    user.email_verified = True
    user.email_verified_at = datetime.utcnow()

    # Mark token as used
    db_token.used_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


def create_reset_token(user_id: str, db: Session) -> str:
    """
    Create a password reset token for a user.

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        Generated token string
    """
    # Invalidate any existing unused reset tokens
    existing_tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user_id,
        PasswordResetToken.used_at.is_(None)
    ).all()

    for token in existing_tokens:
        db.delete(token)

    # Create new token (1 hour expiry)
    token = generate_secure_token()
    expires_at = datetime.utcnow() + timedelta(hours=1)

    db_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(db_token)
    db.commit()

    return token


def verify_reset_token(token: str, db: Session) -> Optional[User]:
    """
    Verify a password reset token.

    Args:
        token: Reset token string
        db: Database session

    Returns:
        User object if token valid, None otherwise
    """
    # Find token
    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()

    if not db_token:
        return None

    # Check if already used
    if db_token.used_at is not None:
        return None

    # Check if expired
    if db_token.expires_at < datetime.utcnow():
        return None

    # Get user
    user = db.query(User).filter(User.id == db_token.user_id).first()

    return user


def mark_reset_token_used(token: str, db: Session) -> bool:
    """
    Mark a password reset token as used.

    Args:
        token: Reset token string
        db: Database session

    Returns:
        True if token marked as used, False otherwise
    """
    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()

    if not db_token:
        return False

    db_token.used_at = datetime.utcnow()
    db.commit()

    return True


def invalidate_all_sessions(user_id: str, db: Session) -> int:
    """
    Invalidate all active sessions for a user (used after password reset).

    Args:
        user_id: User's UUID
        db: Database session

    Returns:
        Number of sessions invalidated
    """
    sessions = db.query(DBSession).filter(DBSession.user_id == user_id).all()
    count = len(sessions)

    for session in sessions:
        db.delete(session)

    db.commit()

    return count
