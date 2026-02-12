#!/usr/bin/env python3
"""
Initialize database tables and test connection to Neon Postgres.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from app.database import engine, Base, Conversation, init_db


def test_connection():
    """Test database connection."""
    print("Testing database connection...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"Connected successfully!")
            print(f"PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False


def create_tables():
    """Create all database tables."""
    print("\nCreating database tables...")
    try:
        init_db()
        print("Tables created successfully!")
        return True
    except Exception as e:
        print(f"Table creation failed: {e}")
        return False


def verify_tables():
    """Verify tables were created."""
    print("\nVerifying tables...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]

            if "conversations" in tables:
                print("✓ 'conversations' table exists")

                result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'conversations'
                    ORDER BY ordinal_position
                """))
                columns = result.fetchall()
                print("\nTable schema:")
                for col_name, col_type in columns:
                    print(f"  - {col_name}: {col_type}")
                return True
            else:
                print("✗ 'conversations' table not found")
                return False
    except Exception as e:
        print(f"Verification failed: {e}")
        return False


def main():
    print("=" * 50)
    print("Physical AI Book - Database Initialization")
    print("=" * 50)

    if not test_connection():
        sys.exit(1)

    if not create_tables():
        sys.exit(1)

    if not verify_tables():
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Database initialization complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
