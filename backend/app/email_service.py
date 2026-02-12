"""
Email service for sending verification and password reset emails.
Uses Python's built-in SMTP library with Gmail.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def send_email(to: str, subject: str, html: str) -> bool:
    """
    Send an email using SMTP.

    Args:
        to: Recipient email address
        subject: Email subject
        html: HTML content of the email

    Returns:
        True if email sent successfully, False otherwise
    """
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", smtp_user)

    if not smtp_user or not smtp_password:
        print("WARNING: SMTP credentials not configured. Email not sent.")
        print(f"Would send to {to}: {subject}")
        return False

    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to

        # Attach HTML content
        html_part = MIMEText(html, "html")
        msg.attach(html_part)

        # Connect and send with timeout to prevent hanging
        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        print(f"Email sent successfully to {to}")
        return True

    except Exception as e:
        print(f"Failed to send email to {to}: {str(e)}")
        return False


def send_verification_email(email: str, token: str) -> bool:
    """
    Send email verification link to user.

    Args:
        email: User's email address
        token: Verification token

    Returns:
        True if email sent successfully
    """
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    verify_url = f"{frontend_url}/verify-email?token={token}"

    subject = "Verify your email - Physical AI Book"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #007bff;
                color: white !important;
                text-decoration: none;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Welcome to Physical AI Book!</h2>
            <p>Thank you for registering. Please verify your email address to complete your registration.</p>
            <p>Click the button below to verify your email:</p>
            <a href="{verify_url}" class="button">Verify Email Address</a>
            <p>Or copy and paste this link into your browser:</p>
            <p><a href="{verify_url}">{verify_url}</a></p>
            <p>This link will expire in 24 hours.</p>
            <div class="footer">
                <p>If you didn't create an account, you can safely ignore this email.</p>
                <p>&copy; 2026 Physical AI Book</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(email, subject, html)


def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset link to user.

    Args:
        email: User's email address
        token: Password reset token

    Returns:
        True if email sent successfully
    """
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    reset_url = f"{frontend_url}/reset-password?token={token}"

    subject = "Reset your password - Physical AI Book"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #dc3545;
                color: white !important;
                text-decoration: none;
                border-radius: 4px;
                margin: 20px 0;
            }}
            .warning {{ background-color: #fff3cd; padding: 12px; border-left: 4px solid #ffc107; margin: 20px 0; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password for your Physical AI Book account.</p>
            <p>Click the button below to reset your password:</p>
            <a href="{reset_url}" class="button">Reset Password</a>
            <p>Or copy and paste this link into your browser:</p>
            <p><a href="{reset_url}">{reset_url}</a></p>
            <div class="warning">
                <strong>Security Note:</strong> This link will expire in 1 hour. After resetting your password,
                all your active sessions will be invalidated and you'll need to log in again.
            </div>
            <div class="footer">
                <p>If you didn't request a password reset, you can safely ignore this email.
                Your password will remain unchanged.</p>
                <p>&copy; 2026 Physical AI Book</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(email, subject, html)
