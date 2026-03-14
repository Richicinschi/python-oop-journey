# Magic Link Authentication System

This document describes the magic link authentication system implemented for the Python OOP Journey website.

## Overview

The authentication system uses passwordless "magic links" sent via email. Users enter their email address, receive a link, click it to authenticate, and receive a JWT token for subsequent requests.

## Architecture

### Backend (FastAPI)

#### Models

- **`User`** (`api/models/user.py`)
  - `id`: UUID primary key
  - `email`: Unique, indexed
  - `display_name`: Optional display name
  - `created_at`, `updated_at`: Timestamps
  - `last_login_at`: Last successful login
  - `last_seen`: Last activity
  - `is_active`: Account status

- **`AuthToken`** (`api/models/auth_token.py`)
  - `id`: UUID primary key
  - `user_id`: Foreign key to users
  - `token_hash`: SHA256 hash of the token (indexed)
  - `expires_at`: Token expiration time
  - `used_at`: When token was consumed (null if unused)
  - `created_at`: Token creation time

#### Services

- **`AuthService`** (`api/services/auth.py`)
  - `create_magic_link(email)`: Generate and store token, return full URL
  - `verify_magic_link(token)`: Validate token, mark used, return user
  - `generate_jwt(user)`: Create JWT access token
  - `verify_jwt(token)`: Decode and validate JWT
  - `revoke_all_user_tokens(user_id)`: Invalidate active tokens

- **`EmailService`** (`api/services/email.py`)
  - `send_magic_link_email(email, link)`: Send branded HTML email
  - Supports SMTP and SendGrid backends
  - Logs to console in development mode

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/magic-link` | Request magic link |
| GET | `/api/v1/auth/verify?token=xxx` | Verify token (from email) |
| POST | `/api/v1/auth/verify` | Verify token (POST body) |
| POST | `/api/v1/auth/refresh` | Refresh JWT before expiry |
| POST | `/api/v1/auth/logout` | Invalidate JWT |
| GET | `/api/v1/auth/me` | Get current user profile |
| PATCH | `/api/v1/auth/me` | Update user profile |

#### Middleware

- **`get_current_user`** (`api/middleware/auth.py`): FastAPI dependency to extract and validate JWT from Authorization header or cookie

### Frontend (Next.js)

#### Context

- **`AuthProvider`** (`contexts/auth-context.tsx`)
  - Manages authentication state
  - Stores JWT in localStorage
  - Provides: `login()`, `verifyToken()`, `logout()`, `refresh()`, `updateProfile()`

#### Components

- **`LoginForm`** (`components/auth/login-form.tsx`): Email input form with validation
- **`UserMenu`** (`components/auth/user-menu.tsx`): Dropdown with profile/logout links
- **`ProtectedRoute`** (`components/auth/protected-route.tsx`): Wrapper for authenticated routes

#### Pages

| Path | Description |
|------|-------------|
| `/auth/login` | Email input form |
| `/auth/callback?token=xxx` | Handle magic link verification |
| `/profile` | User profile management |

#### Middleware

- **`middleware.ts`**: Server-side auth check, redirects unauthenticated users from protected routes

## Security Features

1. **Token Security**
   - Tokens expire in 15 minutes
   - Single-use only (marked as used after verification)
   - Hashed before storage (SHA256)
   - Cryptographically secure random generation (secrets.token_urlsafe)

2. **JWT Security**
   - Expires in 7 days
   - Signed with HS256 algorithm
   - Contains unique JTI (JWT ID) for potential revocation

3. **Rate Limiting**
   - Magic link requests limited to 5 per 15 minutes per IP
   - Implemented with SlowAPI

4. **Email Enumeration Prevention**
   - Always returns success from magic-link endpoint
   - No indication if email exists in system

5. **Cookie Security**
   - HttpOnly cookies recommended for production
   - Secure flag in HTTPS environments
   - SameSite attribute

## Configuration

### Environment Variables

```bash
# JWT
SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_DAYS=7

# Magic Link
MAGIC_LINK_EXPIRE_MINUTES=15
MAGIC_LINK_BASE_URL=http://localhost:3000

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=noreply@oopjourney.com

# Email (SendGrid - preferred for production)
SENDGRID_API_KEY=SG.xxx
```

## Database Migration

```bash
cd apps/api
alembic upgrade head
```

Or manually create tables (development only):
```python
from api.database import init_db
import asyncio
asyncio.run(init_db())
```

## Testing

### Manual Test Flow

1. **Request Magic Link**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/magic-link \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}'
   ```

2. **Check Logs for Link** (development mode shows token)

3. **Verify Token**
   ```bash
   curl "http://localhost:8000/api/v1/auth/verify?token=XXX"
   ```

4. **Access Protected Route**
   ```bash
   curl http://localhost:8000/api/v1/auth/me \
     -H "Authorization: Bearer XXX"
   ```

5. **Logout**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/logout \
     -H "Authorization: Bearer XXX"
   ```

## Development Mode

In development, emails are logged to the console instead of being sent. The magic link endpoint also returns the link in the response for easy testing.

## Production Considerations

1. **Email Provider**: Configure SendGrid or SMTP with valid credentials
2. **Secret Key**: Use a strong, randomly generated secret key
3. **HTTPS**: Ensure all traffic is over HTTPS
4. **Rate Limiting**: Consider Redis-backed rate limiting for distributed deployments
5. **Token Revocation**: Implement Redis denylist for JWT revocation
6. **Monitoring**: Add logging and alerting for failed auth attempts

## Future Enhancements

- OAuth integration (Google, GitHub)
- Multi-factor authentication
- Session management UI
- Admin user management
- Audit logging
