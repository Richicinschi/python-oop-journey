"""Email service for sending magic links and other notifications."""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

import httpx

from api.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# Email template for magic links
MAGIC_LINK_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign in to Python OOP Journey</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f5;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 16px;
        }
        .content {
            padding: 40px 30px;
        }
        .button-container {
            text-align: center;
            margin: 30px 0;
        }
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            text-decoration: none;
            padding: 16px 32px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
        }
        .button:hover {
            box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.4);
        }
        .link-fallback {
            background: #f3f4f6;
            border-radius: 6px;
            padding: 15px;
            word-break: break-all;
            font-family: monospace;
            font-size: 14px;
            color: #4b5563;
            margin: 20px 0;
        }
        .expires {
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin: 20px 0;
        }
        .footer {
            background: #f9fafb;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }
        .footer p {
            margin: 0 0 10px 0;
            color: #6b7280;
            font-size: 14px;
        }
        .footer .ignore {
            color: #9ca3af;
            font-size: 13px;
            margin-top: 15px;
        }
        .icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <div class="icon">🐍</div>
                <h1>Python OOP Journey</h1>
                <p>Master Object-Oriented Programming</p>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>Click the button below to sign in to your Python OOP Journey account:</p>
                
                <div class="button-container">
                    <a href="$magic_link" class="button">Sign In to Your Account</a>
                </div>
                
                <p style="text-align: center; color: #6b7280;">Or copy and paste this link into your browser:</p>
                <div class="link-fallback">$magic_link</div>
                
                <p class="expires">⏰ This link expires in 15 minutes</p>
            </div>
            <div class="footer">
                <p>Need help? Contact us at support@oopjourney.com</p>
                <p class="ignore">
                    Didn't request this email? You can safely ignore it.<br>
                    This magic link was requested for $email.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
""")

TEXT_TEMPLATE = Template("""
Python OOP Journey - Sign In

Click the link below to sign in to your account:

$magic_link

This link expires in 15 minutes.

Didn't request this email? You can safely ignore it.
This magic link was requested for $email.
""")


class EmailService:
    """Service for sending emails via SMTP or SendGrid."""

    def __init__(self):
        self.settings = get_settings()
        self.provider = self._detect_provider()

    def _detect_provider(self) -> str:
        """Detect which email provider to use."""
        if self.settings.sendgrid_api_key:
            return "sendgrid"
        elif self.settings.smtp_host and self.settings.smtp_user:
            return "smtp"
        return "none"

    async def send_magic_link_email(self, email: str, link: str) -> bool:
        """Send magic link email to user.
        
        Args:
            email: Recipient email address
            link: Full magic link URL
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        subject = "Sign in to Python OOP Journey"
        
        # Render templates
        html_content = MAGIC_LINK_TEMPLATE.substitute(
            magic_link=link,
            email=email,
        )
        text_content = TEXT_TEMPLATE.substitute(
            magic_link=link,
            email=email,
        )

        # Send via appropriate provider
        if self.provider == "sendgrid":
            return await self._send_sendgrid(email, subject, html_content, text_content)
        elif self.provider == "smtp":
            return await self._send_smtp(email, subject, html_content, text_content)
        else:
            # Log in development mode
            if self.settings.is_development:
                logger.info(f"[EMAIL] To: {email}")
                logger.info(f"[EMAIL] Subject: {subject}")
                logger.info(f"[EMAIL] Magic Link: {link}")
                return True
            logger.error("No email provider configured")
            return False

    async def _send_sendgrid(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
    ) -> bool:
        """Send email via SendGrid API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={
                        "Authorization": f"Bearer {self.settings.sendgrid_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "personalizations": [
                            {
                                "to": [{"email": to_email}],
                            }
                        ],
                        "from": {"email": self.settings.smtp_from},
                        "subject": subject,
                        "content": [
                            {"type": "text/plain", "value": text_content},
                            {"type": "text/html", "value": html_content},
                        ],
                    },
                )
                response.raise_for_status()
                logger.info(f"Email sent to {to_email} via SendGrid")
                return True
        except Exception as e:
            logger.error(f"SendGrid email failed: {e}")
            return False

    async def _send_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
    ) -> bool:
        """Send email via SMTP."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.settings.smtp_from
            msg["To"] = to_email

            # Attach parts
            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            # Send via SMTP
            with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.smtp_user, self.settings.smtp_password)
                server.sendmail(self.settings.smtp_from, [to_email], msg.as_string())

            logger.info(f"Email sent to {to_email} via SMTP")
            return True
        except Exception as e:
            logger.error(f"SMTP email failed: {e}")
            return False


# Singleton instance
_email_service: EmailService | None = None


def get_email_service() -> EmailService:
    """Get or create email service singleton."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
