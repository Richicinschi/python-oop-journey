# API Endpoint Audit Report

**Project:** website-playground/apps/api  
**Date:** 2026-03-15  
**Scope:** All 17 routers, 80+ endpoints

---

## 1. ROUTER INVENTORY

| Router File | Prefix | Endpoints | Tags |
|------------|--------|-----------|------|
| `activity.py` | `/api/v1` | 4 | activity |
| `ai.py` | `/api/v1` | 6 | ai |
| `auth.py` | `/api/v1/auth` | 7 | auth |
| `bookmarks.py` | `/api/v1` | 6 | bookmarks |
| `csrf.py` | `/api/v1` | 2 | csrf |
| `curriculum.py` | `/api/v1` | 4 | curriculum |
| `drafts.py` | `/api/v1` | 4 | drafts |
| `execute.py` | `/api/v1` | 4 | execution |
| `health.py` | `/health` | 7 | health |
| `progress.py` | `/api/v1` | 6 | progress |
| `projects.py` | `/api/v1` | 7 | projects |
| `recommendations.py` | `/api/v1/recommendations` | 15 | recommendations |
| `submissions.py` | `/api/v1` | 11 | submissions |
| `sync.py` | `/api/v1` | 4 | sync |
| `user.py` | `/api/v1` | 7 | user |
| `verification.py` | `/api/v1` | 4 | verification |
| `main.py` (direct) | `/` | 3 | health, root |

**Total Endpoints: 80+**

---

## 2. ENDPOINT LISTING BY ROUTER

### Activity Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/activity` | `ActivityList` | Get recent activity |
| POST | `/activity` | `Activity` | Log activity |
| GET | `/activity/summary` | `ActivitySummary` | Get activity summary |
| GET | `/activity/stats` | `dict` | Get activity stats |

### AI Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/ai/hint` | `AIHintResponse` | Generate AI hint |
| POST | `/ai/explain-error` | `AIErrorResponse` | Explain error |
| POST | `/ai/code-review` | `CodeReviewResult` | AI code review |
| POST | `/ai/hint-feedback` | `MessageResponse` | Submit hint feedback |
| POST | `/ai/report-hint` | `MessageResponse` | Report problematic hint |
| GET | `/ai/health` | `HealthResponse` | Check AI service health |

### Auth Router (`/api/v1/auth`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/magic-link` | `MagicLinkResponse` | Request magic link |
| GET | `/verify` | `TokenResponse` | Verify magic token |
| POST | `/verify` | `TokenResponse` | Verify magic token (POST) |
| POST | `/refresh` | `TokenResponse` | Refresh access token |
| POST | `/logout` | **NONE** | Logout user |
| GET | `/me` | `UserSchema` | Get current user |
| PATCH | `/me` | `UserSchema` | Update current user |

### Bookmarks Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/bookmarks` | `BookmarkList` | List bookmarks |
| POST | `/bookmarks` | `Bookmark` | Create bookmark |
| DELETE | `/bookmarks/{bookmark_id}` | `None` (204) | Delete bookmark |
| GET | `/bookmarks/check` | `BookmarkCheck` | Check bookmark status |
| PATCH | `/bookmarks/{bookmark_id}` | `Bookmark` | Update bookmark |
| POST | `/bookmarks/toggle` | `BookmarkCheck` | Toggle bookmark |

### CSRF Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/csrf-token` | `CSRFTokenResponse` | Get CSRF token |
| POST | `/csrf-refresh` | `CSRFTokenResponse` | Refresh CSRF token |

### Curriculum Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/curriculum` | `Curriculum` | Get full curriculum |
| GET | `/curriculum/weeks/{slug}` | `Week` | Get single week |
| GET | `/curriculum/problems` | `list[ProblemListItem]` | List all problems |
| GET | `/curriculum/problems/{slug}` | `ProblemDetailResponse` | Get problem details |

### Drafts Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/drafts` | `DraftList` | List all drafts |
| GET | `/drafts/{problem_slug}` | `Draft` | Get draft |
| POST | `/drafts/{problem_slug}` | `Draft` | Save draft |
| DELETE | `/drafts/{problem_slug}` | `None` (204) | Delete draft |

### Execute Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/execute/run` | `CodeExecutionResponse` | Execute Python code |
| POST | `/execute/syntax-check` | `ValidationResponse` | Check code syntax |
| GET | `/execute/health` | `ExecutionHealthResponse` | Execution health check |
| POST | `/execute` | `CodeExecutionResponse` | Execute Python code (legacy) |

### Health Router (`/health`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/health` | `HealthStatus` | Basic health check |
| GET | `/health/detailed` | `HealthCheckDetailed` | Detailed health check |
| GET | `/health/db` | `DBHealthResponse` | Database health check |
| GET | `/health/cache` | `CacheHealthResponse` | Cache health check |
| GET | `/health/ready` | `ReadyResponse` | Readiness probe |
| GET | `/health/live` | `LiveResponse` | Liveness probe |
| GET | `/health/curriculum` | `CurriculumHealthResponse` | Curriculum health check |

### Progress Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/progress` | `ProgressList` | Get all user progress |
| GET | `/progress/{problem_slug}` | `Progress` | Get problem progress |
| POST | `/progress/{problem_slug}` | `Progress` | Update progress |
| POST | `/progress/{problem_slug}/attempt` | `Progress` | Record attempt |
| GET | `/progress/stats/overall` | `ProgressStats` | Get overall stats |
| GET | `/progress/week/{week_slug}` | `WeekProgress` | Get week progress |

### Projects Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/projects/{slug}` | `ProjectMetadata` | Get project metadata |
| POST | `/projects/{slug}/run` | `ProjectExecutionResponse` | Run project |
| POST | `/projects/{slug}/test` | `ProjectTestResult` | Run project tests |
| POST | `/projects/{slug}/validate` | `ProjectValidationResponse` | Validate project |
| POST | `/projects/{slug}/save` | `ProjectSaveResponse` | Save project state |
| POST | `/projects/{slug}/submit` | `ProjectSubmissionResponse` | Submit project |
| GET | `/projects/{slug}/template` | `ProjectTemplate` | Get project template |

### Recommendations Router (`/api/v1/recommendations`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/recommendations/next` | `RecommendationResponse` | Get next recommendation |
| GET | `/recommendations/all` | `list[RecommendationResponse]` | Get all recommendations |
| GET | `/recommendations/review` | `ReviewQueueResponse` | Get review queue |
| GET | `/recommendations/review/stats` | `ReviewStatsResponse` | Get review stats |
| POST | `/recommendations/review/{problem_slug}` | `RecordReviewResponse` | Record review |
| GET | `/recommendations/weak-areas` | `list[WeakAreaResponse]` | Get weak areas |
| GET | `/recommendations/path` | `LearningPathResponse` | Get learning path |
| GET | `/recommendations/difficulty` | `DifficultySuggestionResponse` | Get difficulty suggestion |
| GET | `/recommendations/stats/time` | `dict` | Get time analytics |
| GET | `/recommendations/stats/attempts` | `AttemptPatternResponse` | Get attempt patterns |
| GET | `/recommendations/stats/mastery` | `dict` | Get topic mastery |
| GET | `/recommendations/stats/velocity` | `LearningVelocityResponse` | Get learning velocity |
| GET | `/recommendations/stats/success-rate` | `dict` | Get success rate |
| GET | `/recommendations/stats` | `LearningStatsResponse` | Get learning stats |
| GET | `/recommendations/streak` | `dict` | Get streak info |

### Submissions Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/projects/{project_slug}/submit` | `SubmissionResponse` | Submit project |
| GET | `/projects/{project_slug}/checklist` | `SubmissionChecklist` | Get pre-submission checklist |
| GET | `/submissions` | `SubmissionList` | List submissions |
| GET | `/submissions/{submission_id}` | `Submission` | Get submission |
| GET | `/submissions/{submission_id}/files` | `dict[str, str]` | Get submission files |
| GET | `/admin/reviews/queue` | `ReviewQueue` | Get review queue |
| POST | `/admin/submissions/{submission_id}/review` | `Submission` | Review submission |
| POST | `/admin/reviews/batch` | `BatchReviewResult` | Batch review |
| GET | `/submissions/{submission_id}/comments` | `SubmissionCommentList` | Get comments |
| POST | `/submissions/{submission_id}/comments` | `SubmissionComment` | Add comment |
| GET | `/submissions/gamification/stats` | `GamificationStats` | Get gamification stats |

### Sync Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/sync/batch` | `BatchSyncResponse` | Batch sync operations |
| POST | `/sync/force` | `ForceSyncResponse` | Force sync operation |
| GET | `/sync/status` | `SyncStatusResponse` | Get sync status |
| POST | `/sync/resolve` | `ConflictResolutionResponse` | Resolve sync conflict |

### User Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/users/me` | `User` | Get current user profile |
| GET | `/users/me/stats` | `UserStats` | Get user statistics |
| GET | `/users/me/progress` | `list[ProgressSchema]` | Get user progress |
| POST | `/users/me/progress` | `ProgressSchema` | Update progress |
| GET | `/users/me/drafts` | `list[DraftSchema]` | Get user drafts |
| GET | `/users/me/drafts/{problem_slug}` | `DraftSchema` | Get draft for problem |
| POST | `/users/me/drafts` | `DraftSchema` | Save draft |
| DELETE | `/users/me/drafts/{problem_slug}` | `None` (204) | Delete draft |

### Verification Router (`/api/v1`)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| POST | `/verify` | `VerificationResponse` | Verify solution |
| POST | `/verify/{problem_slug}` | `VerificationResponse` | Verify for specific problem |
| POST | `/validate-syntax` | `SyntaxValidationResponse` | Validate syntax |
| GET | `/test-info/{problem_slug}` | **dict** | Get test information |

### Main App (Direct Routes)
| Method | Path | Response Model | Summary |
|--------|------|----------------|---------|
| GET | `/health` | `dict` | Health check |
| GET | `/ready` | `dict` | Readiness check |
| GET | `/` | `dict` | Root endpoint |

---

## 3. ISSUES FOUND

### 🔴 CRITICAL ISSUES

#### 1. **Missing Response Model** - `GET /test-info/{problem_slug}`
- **Location:** `verification.py:136-194`
- **Issue:** Returns raw `dict` instead of Pydantic model
- **Impact:** No validation, no OpenAPI schema generation
- **Fix:** Create `TestInfoResponse` model

#### 2. **Missing Response Model** - `POST /auth/logout`
- **Location:** `auth.py:309-360`
- **Issue:** Returns raw `dict` (`{"success": True, "message": "..."}`)
- **Impact:** No validation, inconsistent with other auth endpoints
- **Fix:** Create `LogoutResponse` model

#### 3. **Inconsistent Error Handling** - Auth Router
- **Location:** `auth.py`
- **Issue:** `verify_magic_link_get` doesn't expose error details, but `verify_magic_link_post` does
- **Fix:** Standardize error message exposure

### 🟡 MEDIUM PRIORITY ISSUES

#### 4. **Duplicate Response Model Definitions**
- **Location:** `ai.py:36-46` and other routers
- **Issue:** `MessageResponse` and `HealthResponse` defined locally instead of in schemas
- **Fix:** Move to central schema files

#### 5. **Router Prefix Inconsistency**
- **Issue:** Some routers use prefixes in `main.py`, others define full paths
- **Examples:**
  - `health_router` has prefix="/health" in router definition
  - `recommendations_router` has prefix="/recommendations" in router definition  
  - Other routers use full paths like `/activity` in decorators
- **Fix:** Standardize prefix usage

#### 6. **Response Model Mismatch** - `/activity/stats`
- **Location:** `activity.py:91-105`
- **Issue:** Returns `dict` but should return proper schema
- **Fix:** Create `ActivityStats` response model

#### 7. **Path Parameter Type Inconsistency**
- **Issue:** Some endpoints use `str`, others use specific types for path params
- **Example:** `{problem_slug}` vs `{bookmark_id}` both use `str` but bookmarks use explicit ID
- **Fix:** Consider using more specific types where applicable

### 🟢 LOW PRIORITY ISSUES

#### 8. **Missing HTTP Status Code Documentation**
- Several endpoints don't document all possible status codes in `responses` parameter
- **Example:** `POST /auth/verify` documents 401/500 but not 200

#### 9. **Inconsistent Documentation**
- Some endpoints have detailed docstrings with examples
- Others have minimal documentation

#### 10. **WebSocket Not Documented in OpenAPI**
- WebSocket endpoint `/ws/progress` won't appear in Swagger UI
- Expected behavior but worth noting

---

## 4. DUPLICATE ROUTES CHECK

✅ **No exact duplicate routes found**

⚠️ **Overlapping Functionality Detected:**

| Functionality | Primary Route | Secondary Route | Issue |
|--------------|---------------|-----------------|-------|
| Drafts | `/drafts/{problem_slug}` | `/users/me/drafts/{problem_slug}` | Two different paths for same resource |
| Progress | `/progress/{problem_slug}` | `/users/me/progress` | Slightly different scopes |
| User Profile | `/auth/me` | `/users/me` | Different prefixes, same data |
| Health Check | `/health` (main) | `/health` (router) | Both exist but router has prefix |

**Recommendation:** Consider consolidating `/drafts` and `/users/me/drafts` endpoints as they serve the same purpose.

---

## 5. HTTP METHOD VERIFICATION

✅ **All HTTP methods are appropriate for their operations:**

| Operation | Methods Used | Status |
|-----------|--------------|--------|
| Read/List | GET | ✅ Correct |
| Create | POST | ✅ Correct |
| Update | POST, PATCH | ⚠️ Inconsistent |
| Delete | DELETE | ✅ Correct |

**Note:** Some updates use POST instead of PATCH/PUT:
- `POST /progress/{problem_slug}` (should be PATCH)
- `POST /sync/batch` (correct for batch operations)

---

## 6. PATH PARAMETER MATCHING

✅ **All path parameters match their function signatures:**

| Endpoint | Path Param | Function Param | Match |
|----------|------------|----------------|-------|
| `/weeks/{slug}` | `slug` | `slug: str` | ✅ |
| `/problems/{slug}` | `slug` | `slug: str` | ✅ |
| `/progress/{problem_slug}` | `problem_slug` | `problem_slug: str` | ✅ |
| `/bookmarks/{bookmark_id}` | `bookmark_id` | `bookmark_id: str` | ✅ |
| `/drafts/{problem_slug}` | `problem_slug` | `problem_slug: str` | ✅ |
| `/projects/{slug}/...` | `slug` | `slug: str` | ✅ |
| `/submissions/{submission_id}` | `submission_id` | `submission_id: str` | ✅ |
| `/admin/submissions/{submission_id}/review` | `submission_id` | `submission_id: str` | ✅ |
| `/recommendations/review/{problem_slug}` | `problem_slug` | `problem_slug: str` | ✅ |
| `/verify/{problem_slug}` | `problem_slug` | `problem_slug: str` | ✅ |
| `/test-info/{problem_slug}` | `problem_slug` | `problem_slug: str` | ✅ |

---

## 7. ERROR HANDLING ANALYSIS

### ✅ Good Error Handling Examples

**Curriculum Router:**
```python
except HTTPException:
    raise
except ValidationError as e:
    logger.error(...)
    raise HTTPException(status_code=500, detail=...)
except Exception as e:
    logger.error(...)
    raise HTTPException(status_code=500, detail=...)
```

**Auth Router:**
- Catches exceptions and prevents information leakage in production
- Returns generic error messages

### ⚠️ Areas for Improvement

1. **AI Router:** Some endpoints catch generic `Exception` without specific handling
2. **Sync Router:** Some errors logged but not properly propagated
3. **Rate Limiting:** Not all endpoints have rate limiting (should be added to high-cost operations)

---

## 8. RATE LIMITING COVERAGE

### ✅ Endpoints with Rate Limiting

| Endpoint | Rate Limit |
|----------|------------|
| `POST /ai/hint` | 10/hour |
| `POST /ai/explain-error` | 20/hour |
| `POST /ai/code-review` | 5/hour |
| `POST /execute/run` | 30/minute |
| `POST /execute` (legacy) | 30/minute |
| `POST /execute/syntax-check` | 60/minute |
| `POST /verify` | 60/minute |
| `POST /verify/{problem_slug}` | 60/minute |
| `POST /validate-syntax` | 120/minute |
| All AI endpoints (router level) | 100/minute |

### ⚠️ Endpoints WITHOUT Rate Limiting (Should Consider Adding)

- `POST /auth/magic-link` - Email sending (should be limited)
- `POST /auth/verify` - Token verification
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - Logout
- All GET endpoints (generally okay but consider for expensive queries)
- `POST /projects/{slug}/run` - Code execution
- `POST /projects/{slug}/test` - Test execution
- `POST /projects/{slug}/submit` - Project submission

---

## 9. SUMMARY OF FINDINGS

| Category | Count |
|----------|-------|
| **Total Routers** | 17 |
| **Total Endpoints** | 80+ |
| **Critical Issues** | 3 |
| **Medium Issues** | 4 |
| **Low Issues** | 3 |
| **Duplicate Routes** | 0 (exact) / 3 (overlapping) |
| **Missing Rate Limits** | ~20 endpoints |
| **Missing Response Models** | 2 |

### Priority Actions

1. **HIGH:** Add response model to `GET /test-info/{problem_slug}`
2. **HIGH:** Add response model to `POST /auth/logout`
3. **MEDIUM:** Standardize error message handling in auth router
4. **MEDIUM:** Add rate limiting to auth endpoints
5. **MEDIUM:** Consider consolidating duplicate functionality
6. **LOW:** Move inline response models to schema files
7. **LOW:** Document all possible response status codes

---

## 10. SCHEMA VALIDATION STATUS

| Router | All Endpoints Have Response Models |
|--------|-----------------------------------|
| activity.py | ⚠️ No (`/activity/stats` returns dict) |
| ai.py | ✅ Yes (some inline) |
| auth.py | ⚠️ No (`/logout` returns dict) |
| bookmarks.py | ✅ Yes |
| csrf.py | ✅ Yes |
| curriculum.py | ✅ Yes |
| drafts.py | ✅ Yes |
| execute.py | ✅ Yes |
| health.py | ✅ Yes |
| progress.py | ✅ Yes |
| projects.py | ✅ Yes |
| recommendations.py | ✅ Yes |
| submissions.py | ✅ Yes |
| sync.py | ✅ Yes |
| user.py | ✅ Yes |
| verification.py | ⚠️ No (`/test-info` returns dict) |

---

*Report generated by automated API endpoint analysis*
