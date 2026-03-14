#!/usr/bin/env python3
"""
Test script for the magic link authentication system.

This script verifies that all auth system files are in place and
provides instructions for manual testing.
"""

import os
import sys
from pathlib import Path

def check_file(path: str, description: str) -> bool:
    """Check if a file exists."""
    if os.path.exists(path):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description} - {path}")
        return False

def main():
    """Run all checks."""
    print("=" * 70)
    print("Magic Link Authentication System - File Verification")
    print("=" * 70)
    print()
    
    base_dir = Path(__file__).parent
    all_ok = True
    
    # Backend Files
    print("Backend (FastAPI):")
    print("-" * 40)
    
    backend_files = [
        ("apps/api/api/models/user.py", "User model"),
        ("apps/api/api/models/auth_token.py", "AuthToken model"),
        ("apps/api/api/services/auth.py", "Auth service"),
        ("apps/api/api/services/email.py", "Email service"),
        ("apps/api/api/routers/auth.py", "Auth router"),
        ("apps/api/api/middleware/auth.py", "Auth middleware"),
        ("apps/api/api/schemas/user.py", "User schemas"),
        ("apps/api/api/config.py", "Config with auth settings"),
        ("apps/api/migrations/versions/add_users_and_auth_tokens.py", "Alembic migration"),
    ]
    
    for path, desc in backend_files:
        if not check_file(str(base_dir / path), desc):
            all_ok = False
    
    print()
    
    # Frontend Files
    print("Frontend (Next.js):")
    print("-" * 40)
    
    frontend_files = [
        ("apps/web/contexts/auth-context.tsx", "Auth context"),
        ("apps/web/components/auth/login-form.tsx", "Login form component"),
        ("apps/web/components/auth/user-menu.tsx", "User menu component"),
        ("apps/web/components/auth/protected-route.tsx", "Protected route component"),
        ("apps/web/app/auth/login/page.tsx", "Login page"),
        ("apps/web/app/auth/callback/page.tsx", "Auth callback page"),
        ("apps/web/app/profile/page.tsx", "Profile page"),
        ("apps/web/middleware.ts", "Next.js middleware"),
        ("apps/web/components/providers.tsx", "Providers with AuthProvider"),
    ]
    
    for path, desc in frontend_files:
        if not check_file(str(base_dir / path), desc):
            all_ok = False
    
    print()
    print("=" * 70)
    
    if all_ok:
        print("SUCCESS: All auth system files are in place!")
        print()
        print("Next steps:")
        print("1. Install dependencies:")
        print("   cd apps/api && pip install -r requirements.txt")
        print("   cd apps/web && npm install")
        print()
        print("2. Run database migration:")
        print("   cd apps/api")
        print("   alembic upgrade head")
        print()
        print("3. Configure environment variables in apps/api/.env:")
        print("   SECRET_KEY=your-secret-key-min-32-chars")
        print("   SMTP_HOST=smtp.gmail.com (optional)")
        print("   SMTP_USER=your-email@gmail.com (optional)")
        print("   SMTP_PASS=your-app-password (optional)")
        print()
        print("4. Start the servers:")
        print("   cd apps/api && uvicorn api.main:app --reload")
        print("   cd apps/web && npm run dev")
        print()
        print("5. Test the auth flow:")
        print("   - Visit http://localhost:3000/auth/login")
        print("   - Enter an email address")
        print("   - Check API logs for the magic link")
        print("   - Click the link or visit the URL")
        print("   - Verify you're redirected and authenticated")
        return 0
    else:
        print("ERROR: Some files are missing. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
