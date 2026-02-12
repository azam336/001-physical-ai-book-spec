import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not email:
        return False, "Email is required"
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    # Block common disposable email domains
    disposable_domains = ['tempmail.com', 'throwaway.email', '10minutemail.com']
    domain = email.split('@')[1].lower()
    if domain in disposable_domains:
        return False, "Disposable email addresses are not allowed"
    
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""

def sanitize_name(name: str) -> str:
    """Sanitize full name"""
    if not name:
        return ""
    
    # Remove extra whitespace
    name = " ".join(name.split())
    
    # Remove special characters except spaces, hyphens, apostrophes
    name = re.sub(r'[^a-zA-Z\s\-\']', '', name)
    
    # Limit length
    name = name[:255]
    
    return name.strip()

def validate_full_name(name: str) -> Tuple[bool, str]:
    """Validate full name"""
    if not name or len(name.strip()) < 2:
        return False, "Full name must be at least 2 characters"
    
    sanitized = sanitize_name(name)
    if len(sanitized) < 2:
        return False, "Invalid name format"
    
    return True, ""