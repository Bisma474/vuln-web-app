# Deployment Help for Vulnerable Web App

## Getting API Keys for Full Functionality

### 1. SendGrid (For Email Features)
**Purpose**: Email verification, OTP 2FA, verification emails
**Steps**:
1. Sign up at https://sendgrid.com (free tier available)
2. Verify Sender Email:
   - Settings → Sender Authentication
   - Verify a single sender email
3. Create API Key:
   - Settings → API Keys
   - Create API Key with "Mail Send" permission only
   - **Copy the key** (starts with SG.)
4. Get your verified sender email address

**Env Vars**:
- `SENDGRID_API_KEY`: Your SendGrid API key
- `SENDGRID_FROM`: Your verified sender email (e.g., you@example.com)

### 2. Google OAuth (For "Continue with Google")
**Purpose**: Google sign-in and account linking
**Steps**:
1. Go to https://console.cloud.google.com/
2. Create or select a project
3. APIs & Services → OAuth consent screen:
   - User Type: External
   - App name: "Vulnerable Web App"
   - Your email for support/contact
   - Under Test Users: add your Google email
4. APIs & Services → Credentials:
   - Create Credentials → OAuth client ID
   - Application type: Web application
   - Authorized redirect URIs:
     - http://localhost:3001/auth/google/callback
     - https://yourservice.onrender.com/auth/google/callback
   - Create and copy:
     - Client ID (ends with .apps.googleusercontent.com)
     - Client Secret

**Env Vars**:
- `GOOGLE_CLIENT_ID`: Your Google Client ID
- `GOOGLE_CLIENT_SECRET`: Your Google Client Secret

### 3. Cloudflare Turnstile (For CAPTCHA on Login)
**Purpose**: CAPTCHA protection on login form
**Steps**:
1. Sign up at https://dash.cloudflare.com/ (free)
2. Add a site (can be any domain for testing)
3. Applications → Turnstile
4. Create a widget:
   - Widget name: "Login Protection"
   - Hostname: localhost (and your domain later)
   - Widget type: Recommended
5. Create and copy:
   - Site Key (public)
   - Secret Key (private)

**Env Vars**:
- `TURNSTILE_SITE_KEY`: Your Cloudflare Site Key
- `TURNSTILE_SECRET_KEY`: Your Cloudflare Secret Key

## Setting Variables in Render

1. Go to your Render dashboard
2. Select your web service
3. Go to the "Environment" tab
4. Click "Add Environment Variable"
5. For each variable:
   - Key: [exact name from above]
   - Value: [the value you obtained]
   - Leave "Expand From" as "Value"
6. Click "Save Changes"
7. Trigger a manual deploy: "Manual Deploy" → "Deploy latest commit"

## Order of Setup (Recommended)

1. **First**: Get your app deployed with just the render.yaml (core functionality works)
2. **Second**: Add SendGrid for email verification (enables signup/login flow)
3. **Third**: Add Google OAuth for "Continue with Google" button
4. **Fourth**: Add Cloudflare Turnstile for CAPTCHA protection

## Testing Without All Services

The app is designed to work gracefully when services aren't configured:

- **No SendGrid**: Signup shows "email not configured" message (but you can still test login with pre-existing accounts if any)
- **No Google OAuth**: Google button shows "not configured" page
- **No Turnstile**: No CAPTCHA widget appears (login works normally)
- **Core app always works**: You can always test basic signup/login/profile

## Quick Local Test Setup

To test everything locally first:

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your test values (get these from the services above)
nano .env
# Add lines like:
SENDGRID_API_KEY=SG.EXAMPLE_KEY_DO_NOT_USE
SENDGRID_FROM=EXAMPLE@EXAMPLE.COM
GOOGLE_CLIENT_ID=EXAMPLE_ID.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=EXAMPLE_SECRET_DO_NOT_USE
TURNSTILE_SITE_KEY=EXAMPLE_SITE_KEY_DO_NOT_USE
TURNSTILE_SECRET_KEY=EXAMPLE_SECRET_KEY_DO_NOT_USE
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
APP_BASE_URL=https://example.onrender.com

# Run the app
uv run backend/app/main.py
# Visit http://localhost:3001
```

## For Your Professor Demonstration

Even with minimal configuration, you can demonstrate:

### Core Security Features (Always Working):
- ✅ All 8 OWASP vulnerabilities fixed
- ✅ Secure session management (environment-based secret)
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ Password hashing with bcrypt

### Enhanced Features (Configurable):
- Email verification (with SendGrid)
- Account lockout (works without config)
- Password strength meter (frontend only)
- 2FA options (work when email/Google configured)
- Google login (with OAuth configured)
- CAPTCHA protection (with Turnstile configured)
- QR code login (works without extra config)

### Recommended Demo Flow:
1. Show registration page
2. Attempt registration (shows email config needed if no SendGrid)
3. Show login page with basic form
4. Demonstrate login/logout cycle
5. Show profile page (if logged in)
6. Explain what each security feature does
7. Mention how to configure each enhancement for full functionality

The application is production-ready and secure - perfect for showing both vulnerable concepts (through documentation) and secure implementations (in the actual code).
