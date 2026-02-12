from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from slowapi.errors import RateLimitExceeded

from .database import get_db, init_db, Conversation
from .rag import retrieve
from .agent import stream_response
from fastapi import Header, HTTPException, Depends
from datetime import datetime
from typing import Optional
from .auth import (
    hash_password, verify_password, create_session,
    verify_session, delete_session
)
from .validators import validate_email, validate_password, validate_full_name, sanitize_name
from .database import User
from .rate_limiter import limiter, RATE_LIMITS
from .email_service import send_verification_email, send_password_reset_email
from .token_manager import (
    create_verification_token, verify_email_token,
    create_reset_token, verify_reset_token,
    mark_reset_token_used, invalidate_all_sessions
)




app = FastAPI(title="Physical AI Book Assistant")

# Add rate limiter to app state
app.state.limiter = limiter


# Rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str
    selected_text: str | None = None


class HealthResponse(BaseModel):
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    init_db()


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", message="Physical AI Book Assistant is running")


@app.post("/api/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint that retrieves context and streams AI response.
    """
    try:
        retrieved_chunks = retrieve(request.message)
        context_text = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG retrieval failed: {str(e)}")

    async def generate_and_save():
        full_response = []

        try:
            async for chunk in stream_response(
                query=request.message,
                retrieved_chunks=retrieved_chunks,
                selected_text=request.selected_text
            ):
                full_response.append(chunk)
                yield chunk

            conversation = Conversation(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message="".join(full_response),
                context_used=context_text,
                selected_text=request.selected_text
            )
            db.add(conversation)
            db.commit()

        except Exception as e:
            db.rollback()
            yield f"\n\n[Error: {str(e)}]"

    return StreamingResponse(
        generate_and_save(),
        media_type="text/plain"
    )
# Add these imports at the top


# Add these Pydantic models
class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: str

class VerifyEmailRequest(BaseModel):
    token: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

# Add dependency for getting current user
def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    user = verify_session(token, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")
    
    return user

# Add these new endpoints

@app.post("/api/auth/register")
@limiter.limit(RATE_LIMITS["register"])
async def register(
    request: Request,
    request_body: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user and send verification email"""

    # Validate full name
    is_valid, error = validate_full_name(request_body.full_name)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Validate email
    is_valid, error = validate_email(request_body.email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Validate password
    is_valid, error = validate_password(request_body.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request_body.email.lower()).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    hashed_password = hash_password(request_body.password)
    sanitized_name = sanitize_name(request_body.full_name)

    new_user = User(
        full_name=sanitized_name,
        email=request_body.email.lower(),
        password_hash=hashed_password,
        email_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token and send email
    verification_token = create_verification_token(str(new_user.id), db)
    send_verification_email(new_user.email, verification_token)

    # Create session
    token = create_session(str(new_user.id), db)

    return {
        "user": {
            "id": str(new_user.id),
            "full_name": new_user.full_name,
            "email": new_user.email,
            "email_verified": new_user.email_verified,
            "created_at": new_user.created_at.isoformat()
        },
        "token": token
    }

@app.post("/api/auth/login")
@limiter.limit(RATE_LIMITS["login"])
async def login(
    request: Request,
    request_body: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user"""

    # Find user
    user = db.query(User).filter(User.email == request_body.email.lower()).first()

    if not user or not verify_password(request_body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create session
    token = create_session(str(user.id), db)

    return {
        "user": {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "email_verified": user.email_verified,
            "created_at": user.created_at.isoformat()
        },
        "token": token
    }

@app.post("/api/auth/logout")
async def logout(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Logout user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.replace("Bearer ", "")
    delete_session(token, db)

    return {"message": "Logged out successfully"}


@app.post("/api/auth/verify-email")
async def verify_email(request_body: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verify user's email with token"""

    user = verify_email_token(request_body.token, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired verification token"
        )

    return {
        "message": "Email verified successfully",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "email_verified": user.email_verified
        }
    }


@app.post("/api/auth/forgot-password")
@limiter.limit(RATE_LIMITS["password_reset"])
async def forgot_password(
    request: Request,
    request_body: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Request password reset - always returns success for security"""

    # Validate email format
    is_valid, _ = validate_email(request_body.email)
    if not is_valid:
        # Still return success to not reveal if email exists
        return {"message": "If the email exists, a password reset link has been sent"}

    # Find user
    user = db.query(User).filter(User.email == request_body.email.lower()).first()

    # If user exists, send reset email
    if user:
        reset_token = create_reset_token(str(user.id), db)
        send_password_reset_email(user.email, reset_token)

    # Always return success (don't reveal if email exists)
    return {"message": "If the email exists, a password reset link has been sent"}


@app.post("/api/auth/reset-password")
async def reset_password(
    request_body: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password with token"""

    # Validate new password
    is_valid, error = validate_password(request_body.password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)

    # Verify token
    user = verify_reset_token(request_body.token, db)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    # Update password
    user.password_hash = hash_password(request_body.password)
    db.commit()

    # Mark token as used
    mark_reset_token_used(request_body.token, db)

    # Invalidate all sessions (force re-login)
    invalidate_all_sessions(str(user.id), db)

    return {
        "message": "Password reset successfully. Please log in with your new password."
    }


@app.post("/api/auth/resend-verification")
@limiter.limit(RATE_LIMITS["resend_verification"])
async def resend_verification(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resend verification email to current user"""

    if current_user.email_verified:
        raise HTTPException(status_code=400, detail="Email already verified")

    # Create new verification token
    verification_token = create_verification_token(str(current_user.id), db)

    # Send email
    send_verification_email(current_user.email, verification_token)

    return {"message": "Verification email sent"}

@app.get("/api/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at.isoformat()
    }

