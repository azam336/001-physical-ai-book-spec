"""
Rate limiting configuration using slowapi.
Protects authentication endpoints from brute force attacks.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address


# Initialize rate limiter
# Uses in-memory storage by default (suitable for development)
# For production with multiple servers, configure Redis storage:
# limiter = Limiter(
#     key_func=get_remote_address,
#     storage_uri="redis://localhost:6379"
# )
limiter = Limiter(key_func=get_remote_address)


# Rate limit definitions
RATE_LIMITS = {
    "register": "5/hour",      # Max 5 registrations per hour per IP
    "login": "10/minute",       # Max 10 login attempts per minute per IP
    "password_reset": "3/hour", # Max 3 password reset requests per hour per IP
    "resend_verification": "3/hour",  # Max 3 resend verification emails per hour
}
