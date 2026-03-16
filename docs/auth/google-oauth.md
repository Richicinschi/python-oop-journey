# Google OAuth Documentation

## Overview

We use Google OAuth 2.0 for user authentication ("Sign in with Google").

## Setup Process

### 1. Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Create new project: `python-oop-journey`
3. Enable "Google+ API"

### 2. Configure OAuth Consent Screen
1. APIs & Services → OAuth consent screen
2. Select **External** (for public access)
3. Fill in:
   - App name: `Python OOP Journey`
   - User support email: your email
   - Developer contact: your email
4. Add scopes: `openid`, `email`, `profile`
5. Add test users (your email)

### 3. Create OAuth Credentials
1. APIs & Services → Credentials
2. Create OAuth client ID → Web application
3. Name: `OOP Journey Web`
4. Add Authorized JavaScript origins:
   - `http://localhost:3000` (dev)
   - `https://yourdomain.com` (prod)
5. Add Authorized redirect URIs:
   - `http://localhost:3000/auth/callback/google` (dev)
   - `https://yourdomain.com/auth/callback/google` (prod)
6. Save Client ID and Client Secret

## Required Credentials

| Credential | Where to Find | Env Var |
|------------|--------------|---------|
| **Client ID** | Credentials page | `GOOGLE_CLIENT_ID` |
| **Client Secret** | Credentials page (download) | `GOOGLE_CLIENT_SECRET` |

## OAuth Flow

```
1. User clicks "Sign in with Google"
2. Redirect to Google's OAuth page
3. User grants permission
4. Google redirects back with auth code
5. Backend exchanges code for tokens
6. Create/find user in database
7. Issue JWT to frontend
8. User is logged in!
```

## Environment Variables

Set in Render:
```
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx
FRONTEND_URL=https://yourdomain.com
```

## Common Errors

### "redirect_uri_mismatch"
**Cause:** Redirect URI in request doesn't match Google Console

**Fix:** Check Authorized redirect URIs match EXACTLY:
- ✅ `https://yourdomain.com/auth/callback/google`
- ❌ `https://www.yourdomain.com/auth/callback/google`
- ❌ `http://yourdomain.com/auth/callback/google`
- ❌ `https://yourdomain.com/auth/callback/google/`

### "unauthorized_client"
**Cause:** Client ID or Secret is wrong

**Fix:** Copy fresh credentials from Google Console

### "access_denied"
**Cause:** User denied permission

**Fix:** Normal - user chose not to sign in

### "invalid_client"
**Cause:** OAuth consent screen not configured

**Fix:** Complete OAuth consent screen setup

## Testing

Use test users while in development:
1. OAuth consent screen → Test users
2. Add your email
3. Only these emails can sign in until app is verified

## Production Considerations

- App must be verified by Google for public use
- Add privacy policy and terms of service URLs
- Verify domain ownership
- May take 3-5 business days for verification

## Security

- Never expose Client Secret in frontend code
- Use HTTPS in production
- Validate state parameter to prevent CSRF
- Store tokens securely
- Implement proper logout
