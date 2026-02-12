import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from app.database import engine, SessionLocal

def create_auth_tables():
    """Create users and sessions tables"""
    
    # SQL for users table
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        full_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMP DEFAULT NOW(),
        last_login TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    """
    
    # SQL for sessions table
    sessions_table = """
    CREATE TABLE IF NOT EXISTS sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(500) UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
    CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
    """
    
    # SQL to add user_id to conversations (if not exists)
    update_conversations = """
    ALTER TABLE conversations 
    ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE SET NULL;
    
    CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
    """
    
    db = SessionLocal()
    try:
        print("Creating users table...")
        db.execute(text(users_table))
        print("✓ Users table created")
        
        print("Creating sessions table...")
        db.execute(text(sessions_table))
        print("✓ Sessions table created")
        
        print("Updating conversations table...")
        db.execute(text(update_conversations))
        print("✓ Conversations table updated")
        
        db.commit()
        print("\n✅ All authentication tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_auth_tables()