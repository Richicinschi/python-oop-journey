# 🔒 Security Audit Report: Python OOP Journey

**Audit Date:** 2026-03-15  
**Auditor:** Security Engineer Agent  
**Scope:** Frontend (Next.js), Backend (FastAPI), Code Execution System  
**Production URLs:**
- Frontend: https://python-oop-journey.onrender.com
- Backend: https://oop-journey-api.onrender.com

---

## Executive Summary

This security audit identified **1 Critical**, **4 High**, **7 Medium**, and **5 Low** risk vulnerabilities. The most critical issue is the **JWT token storage in localStorage**, which exposes the application to XSS-based token theft. Additionally, several endpoints lack proper rate limiting, and the code execution sandbox has security weaknesses on Windows deployments.

---

## 🔴 Critical Vulnerabilities (Immediate Fix Required)

### 1. JWT Tokens Stored in localStorage (XSS Risk)
**Location:** `website-playground/apps/web/contexts/auth-context.tsx`  
**Severity:** Critical  
**CVSS Score:** 9.1

**Issue:**  
JWT authentication tokens are stored in browser localStorage (lines 51-52, 131, 200, 247):
```typescript
const storedUser = localStorage.getItem(USER_KEY);
const token = localStorage.getItem(TOKEN_KEY);
localStorage.setItem(TOKEN_KEY, data.access_token);
```

**Impact:**  
- Any XSS vulnerability allows immediate theft of authentication tokens
- Tokens are accessible to all JavaScript on the domain
- No HttpOnly protection against script-based attacks
- An attacker gaining script execution can impersonate users indefinitely

**Remediation:**
1. Move token storage to **HttpOnly, Secure, SameSite=Strict cookies**
2. Implement a token refresh mechanism with short-lived access tokens (15 min)
3. Use the existing cookie support in the backend (`request.cookies.get("access_token")` in auth middleware)
4. Update the frontend to rely on cookie-based authentication

```typescript
// Instead of localStorage, let the browser handle cookies automatically
// Backend sets: Set-Cookie: access_token=<jwt>; HttpOnly; Secure; SameSite=Strict; Max-Age=604800
```

---

## 🟠 High Risk Issues (Fix Within 1 Week)

### 2. Weak Default Secret Key in Configuration
**Location:** `website-playground/apps/api/api/config.py` line 24  
**Severity:** High

**Issue:**
```python
secret_key: str = Field(default="dev-secret", description="Secret key for JWT and sessions")
```

**Impact:**
- If `SECRET_KEY` environment variable is not set in production, JWT tokens can be forged
- Attackers can generate valid authentication tokens for any user

**Remediation:**
```python
import secrets

secret_key: str = Field(
    default_factory=lambda: secrets.token_urlsafe(32),
    description="Secret key for JWT and sessions"
)

@field_validator("secret_key")
@classmethod
def validate_secret_key(cls, v: str) -> str:
    if len(v) < 32:
        raise ValueError("Secret key must be at least 32 characters")
    return v
```

---

### 3. No Rate Limiting on Code Execution Endpoints
**Location:** `website-playground/apps/api/api/routers/execute.py`  
**Severity:** High

**Issue:**
The `/api/v1/execute/run` endpoint has no rate limiting, allowing unlimited code execution requests.

**Impact:**
- Resource exhaustion attacks (CPU/memory)
- Potential sandbox escape attempts through brute force
- Denial of Service on the execution service

**Remediation:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/execute/run")
@limiter.limit("30/minute")  # Conservative limit for code execution
async def execute_code(...):
    ...
```

---

### 4. Code Execution Sandbox Weak on Windows
**Location:** `website-playground/apps/api/api/services/simple_execution.py`  
**Severity:** High

**Issue:**
```python
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False
    logger.warning("Resource module not available (Windows or restricted environment).")
```

On Windows, resource limits (memory, CPU) are NOT enforced - only Python-level timeout works.

**Impact:**
- Malicious code can consume unlimited system memory
- Fork bombs can crash the server
- File system access is unrestricted

**Remediation:**
1. Use Docker containers for code execution (already implemented in `project_execution.py`)
2. For Windows, implement additional restrictions:
   - Use Windows Job Objects with memory limits
   - Restrict file system access with sandboxed directories
   - Run in separate low-privilege user context

```python
# For Windows - use job objects
if os.name == 'nt':
    import ctypes
    from ctypes import wintypes
    # Create job object with memory limits
```

---

### 5. Admin Endpoints Lack Admin Role Verification
**Location:** `website-playground/apps/api/api/routers/submissions.py` lines 233-276  
**Severity:** High

**Issue:**
```python
@router.get("/admin/reviews/queue")
async def get_review_queue(
    user: Annotated[User, Depends(get_current_user)],  # Any authenticated user!
    ...
):
    # TODO: Check admin role
    # if not user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
```

**Impact:**
- Any authenticated user can access the admin review queue
- Users can view other users' pending submissions
- Batch review operations are exposed

**Remediation:**
```python
async def require_admin(user: User = Depends(get_current_user)) -> User:
    if not getattr(user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

@router.get("/admin/reviews/queue")
async def get_review_queue(
    user: Annotated[User, Depends(require_admin)],  # Now requires admin
    ...
):
```

Add `is_admin` column to User model if not present.

---

## 🟡 Medium Risk Issues (Fix Within 1 Month)

### 6. Missing CSRF Protection on State-Changing Operations
**Location:** Frontend API calls  
**Severity:** Medium

**Issue:**
No CSRF tokens are used for state-changing operations. While JWT in Authorization header provides some protection, cookie-based auth (which is also supported) is vulnerable to CSRF.

**Remediation:**
1. If using cookie-based auth, implement Double Submit Cookie pattern:
```typescript
// Add CSRF token to all state-changing requests
const csrfToken = getCsrfToken(); // From cookie or meta tag
fetch('/api/v1/progress/...', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrfToken,
  },
});
```

2. Or ensure all state-changing requests use `Authorization: Bearer` header only

---

### 7. CORS Allows All Origins with Credentials
**Location:** `website-playground/apps/api/api/main.py` lines 72-78  
**Severity:** Medium

**Issue:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # But defaults are broad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

In `config.py`, the default origins include multiple domains without strict validation.

**Impact:**
- Potential for cross-origin attacks if any allowed origin is compromised
- Credentials can be sent to unexpected origins

**Remediation:**
```python
# In production, strictly validate origins
@property
def allowed_origins(self) -> List[str]:
    origins = [origin.strip() for origin in self.allowed_origins_raw.split(",")]
    if self.is_production:
        # Validate no localhost or wildcard origins in production
        for origin in origins:
            if "localhost" in origin or "*" in origin:
                raise ValueError(f"Invalid origin in production: {origin}")
    return origins
```

---

### 8. WebSocket Authentication Bypass
**Location:** `website-playground/apps/api/api/main.py` lines 116-121  
**Severity:** Medium

**Issue:**
```python
@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    user_id = websocket.query_params.get("user_id", "anonymous")  # No validation!
    await ProgressWebSocket.handle(websocket, user_id)
```

**Impact:**
- Any client can connect as any user_id
- Can receive other users' progress updates
- Can send spoofed progress updates

**Remediation:**
```python
@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    # Extract and validate token from query param or cookie
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return
    
    auth_service = AuthService(db)
    payload = auth_service.verify_jwt(token)
    if not payload:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    user_id = payload["sub"]
    await ProgressWebSocket.handle(websocket, user_id)
```

---

### 9. Information Disclosure in Error Messages
**Location:** Multiple endpoints  
**Severity:** Medium

**Issue:**
```python
@app.get("/ready")
async def readiness_check():
    except Exception as e:
        db_status = f"error: {str(e)}"  # Full error exposed!
```

**Impact:**
- Stack traces and internal errors may leak sensitive information
- Database connection details exposed

**Remediation:**
```python
@app.get("/ready")
async def readiness_check():
    try:
        ...
    except Exception:
        logger.exception("Database health check failed")  # Log internally
        return {
            "status": "not_ready",
            "database": "error",  # Generic message to client
        }, 503
```

---

### 10. AI Prompt Injection Vulnerability
**Location:** `website-playground/apps/api/api/services/ai_hints.py` lines 189-218  
**Severity:** Medium

**Issue:**
```python
async def _is_content_safe(self, content: str) -> tuple[bool, str]:
    # Simple keyword-based checks only
    unsafe_patterns = [
        r"ignore\s+(previous|earlier|above)\s+instructions",
        ...
    ]
```

**Impact:**
- Users can potentially manipulate AI prompts
- AI could be instructed to generate harmful content
- System prompts may be leaked

**Remediation:**
1. Implement stronger input validation
2. Use AI-based safety checking (commented out in code)
3. Add output filtering for sensitive patterns
4. Implement user input sanitization before sending to AI

---

### 11. File Path Traversal in Project Execution
**Location:** `website-playground/apps/api/api/services/project_execution.py` line 640-647  
**Severity:** Medium

**Issue:**
```python
def _sanitize_path(self, path: str) -> str:
    path = os.path.normpath(path)
    path = path.lstrip("/\\")
    path = path.replace("..", "_")  # Single replacement only!
    return path
```

**Impact:**
- Path traversal via encoded sequences: `..%2f..%2fetc%2fpasswd`
- Double encoding: `....//....//etc/passwd`

**Remediation:**
```python
def _sanitize_path(self, path: str) -> str:
    import urllib.parse
    # Decode first
    path = urllib.parse.unquote(path)
    # Normalize
    path = os.path.normpath(path)
    # Ensure it doesn't escape base directory
    if path.startswith("/") or path.startswith("\\") or ".." in path:
        raise ValueError("Invalid path")
    return path
```

---

### 12. Magic Link Token Exposure in Development
**Location:** `website-playground/apps/api/api/routers/auth.py` lines 58-64  
**Severity:** Medium

**Issue:**
```python
if settings.is_development:
    response["debug"] = {
        "magic_link": magic_link,  # Full link exposed!
        "email_sent": email_sent,
    }
```

While only in development, this can lead to accidental exposure if `is_development` is misconfigured.

**Remediation:**
```python
# Remove debug endpoints entirely or use explicit debug mode
if settings.debug_mode_explicit:  # Must be explicitly enabled
    logger.debug(f"Magic link generated: {magic_link}")  # Log only, don't return
```

---

## 🟢 Low Risk Issues (Fix When Convenient)

### 13. Missing Security Headers on API
**Location:** `website-playground/apps/api/api/main.py`  
**Severity:** Low

**Issue:**
No security headers middleware configured for FastAPI.

**Remediation:**
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["python-oop-journey.onrender.com", "oop-journey-api.onrender.com"]
)
```

---

### 14. No Input Length Validation on Comments
**Location:** `website-playground/apps/api/api/routers/submissions.py`  
**Severity:** Low

**Issue:**
Submission comments have no length validation, potentially allowing storage abuse.

**Remediation:**
Add to schema:
```python
class SubmissionCommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
```

---

### 15. JWT Algorithm Not Explicitly Restricted
**Location:** `website-playground/apps/api/api/services/auth.py` lines 166-184  
**Severity:** Low

**Issue:**
```python
payload = jwt.decode(
    token, settings.secret_key, algorithms=[settings.jwt_algorithm]
)
```

If an attacker can control `jwt_algorithm` environment variable, they could use the `none` algorithm.

**Remediation:**
```python
# Hardcode allowed algorithms
ALLOWED_ALGORITHMS = ["HS256", "HS384", "HS512"]

payload = jwt.decode(
    token, 
    settings.secret_key, 
    algorithms=ALLOWED_ALGORITHMS
)
```

---

### 16. SQL Injection Risk in Raw Queries
**Location:** `website-playground/apps/api/api/main.py` line 150  
**Severity:** Low

**Issue:**
```python
await db.execute("SELECT 1")
```

While currently safe, raw SQL usage should be minimized.

**Remediation:**
Use SQLAlchemy text() for raw queries or prefer ORM methods.

---

### 17. No Account Lockout Mechanism
**Location:** Authentication system  
**Severity:** Low

**Issue:**
No protection against brute force attacks on magic link or token verification.

**Remediation:**
Implement account lockout after failed attempts:
```python
# Track failed attempts in Redis/cache
if failed_attempts > 5:
    raise HTTPException(
        status_code=429,
        detail="Too many failed attempts. Try again later."
    )
```

---

## 📊 Security Scorecard

| Category | Score | Notes |
|----------|-------|-------|
| Authentication | ⚠️ 5/10 | JWT in localStorage is critical flaw |
| Authorization | ⚠️ 6/10 | Admin checks missing |
| Input Validation | ✅ 7/10 | Pydantic schemas good, some gaps |
| Output Encoding | ✅ 8/10 | Proper JSON serialization |
| Session Management | ⚠️ 5/10 | Token storage issue |
| Error Handling | ⚠️ 6/10 | Some info leakage |
| Logging | ✅ 7/10 | Good logging coverage |
| Code Execution | ⚠️ 5/10 | Windows sandbox weak |
| Cryptography | ✅ 7/10 | Standard libraries used |
| **Overall** | **⚠️ 6/10** | **Needs improvement** |

---

## 🎯 Priority Remediation Roadmap

### Week 1 (Critical)
1. **Move JWT from localStorage to HttpOnly cookies**
2. **Enforce strong SECRET_KEY in production**
3. **Add rate limiting to execute endpoints**

### Week 2 (High)
4. **Implement admin role verification**
5. **Fix Windows sandbox resource limits**
6. **Secure WebSocket authentication**

### Month 1 (Medium)
7. **Implement CSRF protection**
8. **Strengthen CORS configuration**
9. **Fix path traversal vulnerability**
10. **Improve error message sanitization**

### Month 2 (Low)
11. **Add security headers middleware**
12. **Implement account lockout**
13. **AI safety improvements**
14. **Input length validations**

---

## 🔍 Testing Recommendations

### Automated Security Testing
```yaml
# Add to CI/CD pipeline
- name: Run Bandit (Python SAST)
  run: bandit -r api/

- name: Run npm audit
  run: npm audit --audit-level high

- name: Run OWASP ZAP scan
  uses: zaproxy/action-baseline@v0.7.0
```

### Manual Penetration Testing
1. Test XSS payloads in all input fields
2. Verify CSRF protection on all state-changing endpoints
3. Attempt path traversal in project file uploads
4. Test rate limiting with automation tools
5. Verify WebSocket authentication isolation

---

## 📚 References

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP JWT Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)

---

*Report generated by Security Engineer Agent*  
*For questions or clarifications, please review the specific file locations and remediation code provided.*
