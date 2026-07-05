# How to Get Google OAuth Credentials for Your Vulnerable Web App

## Step-by-Step Guide

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top and select "New Project"
4. Enter a project name (e.g., "vuln-web-app-oauth")
5. Click "Create"

### 2. Enable the Required APIs
1. With your project selected, go to "APIs & Services" > "Library"
2. Search for and enable:
   - Google+ API (or Google People API)
   - Google+ Domains API (if needed)
   - Alternatively, just enable "Google+ API" for basic profile info

### 3. Create OAuth 2.0 Client ID
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted to configure consent screen:
   - Select "External" user type
   - Click "Create"
   - Fill in:
     * App name: "Vulnerable Web App"
     * User support email: Your email
     * Developer contact email: Your email
   - Skip scopes for now (click "Save and Continue")
   - Add yourself as a test user (click "Add Users" under Test users)
   - Click "Save and Continue" then "Back to Dashboard"
4. Back in Credentials, click "Create Credentials" > "OAuth client ID"
5. Select "Web application" as the application type
6. Fill in:
   - Name: "Vuln Web App Render"
   - Authorized JavaScript origins: 
     * Leave blank for now (not needed for server-side flow)
   - Authorized redirect URIs:
     * `https://your-app.onrender.com/auth/google/callback`
     * Replace `your-app` with your actual Render service name
     * For local testing, you can also add: `http://localhost:3001/auth/google/callback`
7. Click "Create"

### 4. Copy Your Credentials
1. After creation, you'll see:
   - Client ID: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com`
   - Client secret: `GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. Copy both values - you'll need these for your .env file

### 5. Add to Your Render Environment Variables
1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add these variables:
   - Key: `GOOGLE_CLIENT_ID`
     Value: [paste your Client ID here]
   - Key: `GOOGLE_CLIENT_SECRET`
     Value: [paste your Client secret here]
5. Click "Save Changes"

### 6. Trigger a Redeploy
1. In your Render service dashboard, click "Manual Deploy"
2. Select "Deploy latest commit"
3. Wait for the redeploy to complete

### 7. Test the Google Login
1. Visit your deployed app URL
2. Click "Continue with Google" button
3. You should be redirected to Google's sign-in page
4. After successful login, you should be redirected back to your app

## Important Notes
- Keep your Client Secret secure - never commit it to git
- The redirect URI must exactly match what you configured in Google Cloud
- For Render, your URL will be: `https://yourservice.onrender.com`
- You can test locally first by adding `http://localhost:3001/auth/google/callback` to authorized redirect URIs
- Google may show a "This app isn't verified" warning - this is normal for testing; click "Advanced" then "Go to [your app] (unsafe)"

## Troubleshooting
- **redirect_uri_mismatch**: Double-check your authorized redirect URI matches exactly
- **access_denied**: Make sure you're added as a test user in the OAuth consent screen
- **invalid_client**: Verify your Client ID and Secret are correct
- **invalid_request**: Ensure you've enabled the necessary APIs in Google Cloud Console

Once configured, Google login will allow users to:
1. Sign up with their Google account (automatically verified)
2. Link existing accounts with matching Google email
3. Log in using Google OAuth without needing email verification
