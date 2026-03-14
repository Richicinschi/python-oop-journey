# Google OAuth Setup - Ultra Detailed Tutorial

**Every single click explained with screenshots descriptions.**

Estimated time: 15-20 minutes  
Cost: $0

---

## Overview

Google OAuth lets users sign in with their Google account (Gmail, YouTube, etc.) instead of creating a password.

**What we're doing:**
1. Create a Google Cloud project
2. Enable the API that handles logins
3. Configure what users see when they sign in
4. Create credentials (like a password for your app to talk to Google)
5. Add your website URLs

---

## Step 1: Create Google Cloud Project

### 1.1 Go to Google Cloud Console

1. Open your browser
2. Go to: **https://console.cloud.google.com**
3. You should see this:

```
┌─────────────────────────────────────────────────────────┐
│  Google Cloud Console                                   │
│                                                          │
│  [Google Logo]  Console                                  │
│                                                          │
│  Welcome to Google Cloud!                                │
│                                                          │
│  Select a project ▼                                      │
│  [Dropdown with "NEW PROJECT" button]                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Create New Project

1. Click the **"Select a project"** dropdown at the top
2. A popup appears with a list of projects (if you have any)
3. Click **"NEW PROJECT"** button (top right of the popup)

```
┌─────────────────────────────┐
│  Select a project           │
│                             │
│  [Search projects...]       │
│                             │
│  My Projects                │
│  (list if any)              │
│                             │
│  [+] NEW PROJECT  ← CLICK   │
└─────────────────────────────┘
```

4. You'll see the "New Project" page:

```
┌─────────────────────────────────────────┐
│  New Project                            │
│                                          │
│  Project name *                         │
│  [________________________]  ← TYPE HERE│
│                                          │
│  Organization (optional)                │
│  [No organization ▼]                    │
│                                          │
│  Location                                │
│  [No organization ▼]                    │
│                                          │
│                              [CANCEL] [CREATE]│
└─────────────────────────────────────────┘
```

5. **Type the project name:** `python-oop-journey`
6. **Leave "Organization" as "No organization"**
7. **Leave "Location" as default**
8. Click **"CREATE"**

9. Wait 5-10 seconds. You'll see a notification:
   ```
   ✓ Creating project "python-oop-journey"...
   ```

10. After it's created, you'll be redirected to the dashboard

---

## Step 2: Enable Google+ API

This API is required for OAuth to work.

### 2.1 Open API Library

1. Look for the **hamburger menu (☰)** at top left
2. Click it

```
☰ Navigation menu
```

3. A sidebar opens. Look for **"APIs & Services"**
4. Hover over it, then click **"Library"**

```
Navigation Menu:
┌─────────────────────────────┐
│  ☰                          │
│  HOME                       │
│  MARKETPLACE                │
│  BILLING                    │
│  APIs & Services ▶          │
│    → Library     ← CLICK    │
│    → Enabled APIs & services│
│    → Credentials            │
│    → OAuth consent screen   │
│  ...                        │
└─────────────────────────────┘
```

### 2.2 Search for the API

1. You're now on "API Library" page
2. **Search box at top:** Type `Google+ API`

```
┌─────────────────────────────────────────┐
│  API Library                            │
│                                          │
│  [Search for APIs and services...]      │
│        ↑ Type "Google+ API" here        │
│                                          │
│  Maps                                   │
│  Machine learning                       │
│  ...                                    │
└─────────────────────────────────────────┘
```

3. Results appear. Find **"Google+ API"**
4. Click on it

```
┌─────────────────────────────────────────┐
│  Search Results                         │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │  Google+ API                    │    │
│  │  ★ 4.1 • Social                 │    │
│  │                                 │    │
│  │  [ENABLE]  ← CLICK THIS BUTTON  │    │
│  └─────────────────────────────────┘    │
│                                          │
│  Other results...                        │
└─────────────────────────────────────────┘
```

5. Click the **"ENABLE"** button
6. Wait 10-20 seconds for it to enable
7. You'll see a loading spinner, then:
   ```
   ✓ API enabled
   ```

---

## Step 3: Configure OAuth Consent Screen

This is what users see when they click "Sign in with Google"

### 3.1 Go to OAuth Consent Screen

1. Hamburger menu (☰) again
2. **APIs & Services** → **OAuth consent screen**

```
Navigation Menu:
┌─────────────────────────────┐
│  APIs & Services ▶          │
│    → Library                │
│    → Enabled APIs & services│
│    → Credentials            │
│    → OAuth consent screen   │
│              ↑ CLICK        │
└─────────────────────────────┘
```

### 3.2 Select User Type

You'll see:

```
┌─────────────────────────────────────────┐
│  OAuth consent screen                   │
│                                          │
│  User Type                               │
│                                          │
│  (•) Internal   - Only for your org     │
│  ( ) External   - For any Google user   │
│                                          │
│  Select [Internal] or [External]:       │
│                                          │
│                              [CREATE]   │
└─────────────────────────────────────────┘
```

**Click:** **"External"** radio button

**Why External?** Because you want anyone with a Google account to be able to sign in, not just people in your company.

Then click **"CREATE"**

### 3.3 Fill App Information

You'll see a form:

```
┌─────────────────────────────────────────┐
│  Edit app registration                  │
│                                          │
│  App information                         │
│  ─────────────────                       │
│                                          │
│  App name *                             │
│  [________________________________]     │
│                                          │
│  User support email *                   │
│  [________________________________]     │
│                                          │
│  App logo (optional)                    │
│  [UPLOAD IMAGE]                         │
│  (Skip this for now)                    │
│                                          │
│  [SAVE AND CONTINUE]                    │
└─────────────────────────────────────────┘
```

**Fill in:**

| Field | Value |
|-------|-------|
| **App name** | `Python OOP Journey` |
| **User support email** | your Gmail address |

**Don't upload a logo yet** - you can add one later.

Click **"SAVE AND CONTINUE"**

### 3.4 Scopes (What permissions you need)

You'll see:

```
┌─────────────────────────────────────────┐
│  Scopes                                 │
│                                          │
│  Add or remove scopes to specify what   │
│  data your app can access...            │
│                                          │
│  [ADD OR REMOVE SCOPES]  ← CLICK        │
│                                          │
│  [SAVE AND CONTINUE]                    │
└─────────────────────────────────────────┘
```

1. Click **"ADD OR REMOVE SCOPES"**

A modal/popup appears:

```
┌─────────────────────────────────────────┐
│  Update selected scopes                 │
│                                          │
│  [Filter...]                            │
│                                          │
│  ☑ openid                               │
│  ☑ email                                │
│  ☑ profile                              │
│  ☐ other scopes...                      │
│                                          │
│  [CANCEL]  [UPDATE]                     │
└─────────────────────────────────────────┘
```

2. **Check these 3 boxes:**
   - ✅ `openid`
   - ✅ `email` 
   - ✅ `profile`

3. Click **"UPDATE"**

4. Back on Scopes page, click **"SAVE AND CONTINUE"**

### 3.5 Test Users (Optional but Recommended)

```
┌─────────────────────────────────────────┐
│  Test users                             │
│                                          │
│  While your app is in testing...        │
│                                          │
│  [ADD USERS]  ← CLICK                   │
│                                          │
│  [SAVE AND CONTINUE]                    │
└─────────────────────────────────────────┘
```

1. Click **"ADD USERS"**
2. Enter your Gmail address
3. Click **"ADD"**
4. Click **"SAVE AND CONTINUE"**

**Why?** While in "Testing" mode, only these users can sign in. This prevents random people from using your app before it's ready.

### 3.6 Summary

You'll see a summary page. Just click **"BACK TO DASHBOARD"**

---

## Step 4: Create OAuth Credentials

This creates the "password" your app uses to talk to Google.

### 4.1 Go to Credentials

1. Hamburger menu (☰)
2. **APIs & Services** → **Credentials**

```
┌─────────────────────────────────────────┐
│  Credentials                            │
│                                          │
│  API Keys       0                       │
│  OAuth 2.0      0  ← We need to create  │
│  Service Accounts 0                     │
│                                          │
│  [+ CREATE CREDENTIALS]  ← CLICK        │
│                                          │
└─────────────────────────────────────────┘
```

### 4.2 Create OAuth Client ID

1. Click **"+ CREATE CREDENTIALS"**
2. Select **"OAuth client ID"**

```
Dropdown menu:
┌─────────────────────────┐
│  + CREATE CREDENTIALS   │
│                         │
│  → API key              │
│  → OAuth client ID  ←   │
│  → Service account      │
│  → Help me choose       │
└─────────────────────────┘
```

### 4.3 Configure OAuth Client

You'll see:

```
┌─────────────────────────────────────────┐
│  Create OAuth client ID                 │
│                                          │
│  Application type *                     │
│  [Select application type ▼]            │
│                                          │
│  Name                                   │
│  [________________________________]     │
│                                          │
│  [CANCEL]  [CREATE]                     │
└─────────────────────────────────────────┘
```

**Fill in:**

1. **Application type:** Select **"Web application"**

2. **Name:** `OOP Journey Web`

3. **Authorized JavaScript origins:**
   - Click **"+ ADD URI"**
   - Type: `http://localhost:3000`
   - This is for local development

4. **Authorized redirect URIs:**
   - Click **"+ ADD URI"**
   - Type: `http://localhost:3000/auth/callback/google`
   - This is where Google sends users after login

```
┌─────────────────────────────────────────┐
│  Application type: Web application ✓    │
│                                          │
│  Name: OOP Journey Web                  │
│                                          │
│  Authorized JavaScript origins:         │
│  1. http://localhost:3000               │
│  [+ ADD URI]                            │
│                                          │
│  Authorized redirect URIs:              │
│  1. http://localhost:3000/auth/callback/google│
│  [+ ADD URI]                            │
│                                          │
│  [CANCEL]  [CREATE]                     │
└─────────────────────────────────────────┘
```

5. Click **"CREATE"**

### 4.4 Save Your Credentials! ⚠️ IMPORTANT

A popup appears with your credentials:

```
┌─────────────────────────────────────────┐
│  OAuth client created                   │
│  ✓                                      │
│                                          │
│  Your Client ID                         │
│  123456789-abc123.apps.googleusercontent.com│
│  [📋 Copy]  ← CLICK THIS                │
│                                          │
│  Your Client Secret                     │
│  •••••••••••••••                       │
│  [📋 Copy]  ← CLICK THIS                │
│                                          │
│  [DOWNLOAD JSON]  ← ALSO CLICK THIS     │
│                                          │
│                              [OK]       │
└─────────────────────────────────────────┘
```

**DO THIS NOW:**

1. **Click the copy icon** next to **Client ID** → Paste somewhere safe
2. **Click the copy icon** next to **Client Secret** → Paste somewhere safe
3. **Click "DOWNLOAD JSON"** → Save the file as `client_secret.json`

**⚠️ WARNING:** You cannot see the Client Secret again after closing this popup!

4. Click **"OK"**

---

## Step 5: Add Production URLs (After Deployment)

**Do this AFTER you've deployed to Fly.io and have your domain working.**

### 5.1 Edit Credentials

1. Go back to **APIs & Services** → **Credentials**
2. Find your OAuth 2.0 Client ID: `OOP Journey Web`
3. Click the **pencil icon** ✏️ (Edit)

### 5.2 Add Your Domain

Add these URIs:

**Authorized JavaScript origins:**
- `https://richicinschi.com`
- `https://www.richicinschi.com` (if you use www)

**Authorized redirect URIs:**
- `https://richicinschi.com/auth/callback/google`
- `https://www.richicinschi.com/auth/callback/google`

Click **"SAVE"**

---

## What You Should Have Now

| Item | Value | Where to Find |
|------|-------|---------------|
| **Client ID** | `xxx.apps.googleusercontent.com` | Credentials page |
| **Client Secret** | `GOCSPX-xxx` | Credentials page (download JSON) |
| **Project ID** | `python-oop-journey` | Top of page |

---

## Common Errors & Fixes

### Error: "redirect_uri_mismatch"
**Cause:** The redirect URI in your code doesn't match Google Console

**Fix:** Make sure these match EXACTLY:
- `https://richicinschi.com/auth/callback/google` ✓
- NOT `http://` (must be `https://`)
- NOT with trailing slash `/`
- NOT `www` if you didn't add it

### Error: "App is not verified"
**Cause:** You're in "Testing" mode and the user isn't in your test users list

**Fix:** 
- Add their email to test users, OR
- Click "Advanced" → "Go to python-oop-journey (unsafe)"

### Error: "Invalid client"
**Cause:** Wrong Client ID or Secret

**Fix:** Double-check you copied them correctly (no extra spaces)

---

## Next Steps

1. **Copy your Client ID and Client Secret** to your notes
2. **Continue with Step 6 in the main tutorial** (Deploy Backend to Fly.io)
3. **You'll paste these into:**
   ```bash
   fly secrets set GOOGLE_CLIENT_ID="your-client-id"
   fly secrets set GOOGLE_CLIENT_SECRET="your-client-secret"
   ```

---

**Questions?** The most common issue is mismatched redirect URIs. Double-check they match exactly!
