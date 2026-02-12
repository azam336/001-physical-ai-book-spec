"""
Migration script to add email verification and password reset functionality.

This script:
1. Adds email_verified and email_verified_at columns to users table
2. Creates email_verification_tokens table
3. Creates password_reset_tokens table
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine, Base, User, EmailVerificationToken, PasswordResetToken

def run_migration():
    """Run the database migration"""

    print("Starting migration...")

    # First, create all base tables if they don't exist
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("OK - All tables created or already exist")

    # Check if email_verified column already exists
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='email_verified'
        """))

        if result.fetchone() is None:
            print("Adding email_verified and email_verified_at columns to users table...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
                ADD COLUMN email_verified_at TIMESTAMP
            """))
            conn.commit()
            print("OK - Added email verification columns to users table")
        else:
            print("OK - Email verification columns already exist in users table")

    print("\nMigration completed successfully!")
    print("\nDatabase ready with:")
    print("  - users table (with email verification fields)")
    print("  - sessions table")
    print("  - email_verification_tokens table")
    print("  - password_reset_tokens table")
    print("  - conversations table")

if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"\nERROR - Migration failed: {str(e)}")
        sys.exit(1)
